from IPython.kernel.zmq.kernelbase import Kernel
from IPython.core.displaypub import publish_display_data
from pexpect import replwrap

import signal
from subprocess import check_output
import tempfile
import re
from glob import glob
from shutil import rmtree

__version__ = '0.1'

version_pat = re.compile(r'Version (\d+(\.\d+)+)')

class GDLKernel(Kernel):
    implementation = 'gdl_kernel'
    implementation_version = __version__
    language = 'GDL'
    @property
    def language_version(self):
        m = version_pat.search(self.banner)
        return m.group(1)

    _banner = None
    @property
    def banner(self):
        if self._banner is None:
            self._banner = check_output(['gdl', '--version']).decode('utf-8')
        return self._banner
    
    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        # Signal handlers are inherited by forked processes, and we can't easily
        # reset it from the subprocess. Since kernelapp ignores SIGINT except in
        # message handlers, we need to temporarily reset the SIGINT handler here
        # so that bash and its children are interruptible.
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            self.gdlwrapper = replwrap.REPLWrapper("gdl",u"GDL> ",None)
            self.gdlwrapper.run_command("!quiet=1 & defsysv,'!inline',0".rstrip(), timeout=None)
        finally:
            signal.signal(signal.SIGINT, sig)

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payloads': [], 'user_expressions': {}}

        interrupted = False
        tfile = tempfile.NamedTemporaryFile(mode='w+t')
        plot_dir = tempfile.mkdtemp()
        plot_format = 'png'

        precall='''
        if !inline then begin
            set_plot,'z'
            device, z_buffering = 1
        endif
        '''

        postcall = '''
        if !inline then begin
            ; load color table info
            tvlct, r_m9QVFuGP,g_jeeyfQkN,b_mufcResT, /get
        
            img_bGr4ea3s = tvrd()

            outfile_c5BXq4dV = '%(plot_dir)s/__fig.png'
            ; Set the colors for each channel
            s_m77YL7Gd = size(img_bGr4ea3s)
            ii_rsApk4JS=bytarr(3,s_m77YL7Gd[1],s_m77YL7Gd[2])
            ii_rsApk4JS[0,*,*]=r_m9QVFuGP[img_bGr4ea3s]
            ii_rsApk4JS[1,*,*]=g_jeeyfQkN[img_bGr4ea3s]
            ii_rsApk4JS[2,*,*]=b_mufcResT[img_bGr4ea3s]

            ; Write the PNG if the image is not blank
            if total(img_bGr4ea3s) ne 0 then begin
                write_png, outfile_c5BXq4dV, ii_rsApk4JS, r_m9QVFuGP, g_jeeyfQkN, b_mufcResT
            endif
        endif
        end
        ''' % locals()

        try:
            tfile.file.write(precall+code.rstrip()+postcall.rstrip())
            tfile.file.close()
            output = self.gdlwrapper.run_command(".run "+tfile.name, timeout=None)

            # Publish images (only one for now)
            images = [open(imgfile, 'rb').read() for imgfile in glob("%s/__fig.png" % plot_dir)]

            display_data=[]

            for image in images:
                display_data.append(('GDL', {'image/png': image}))

            for source, data in display_data:
                publish_display_data(data,source=source)
        except KeyboardInterrupt:
            self.gdlwrapper.child.sendintr()
            interrupted = True
            self.gdlwrapper._expect_prompt()
            output = self.gdlwrapper.child.before
        finally:
            tfile.close()
            rmtree(plot_dir)

        if not silent:
            stream_content = {'name': 'stdout', 'data':output}
            self.send_response(self.iopub_socket, 'stream', stream_content)
        
        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}
        
        try:
            exitcode = int(self.run_command('print,0').rstrip())
        except Exception:
            exitcode = 1

        if exitcode:
            return {'status': 'error', 'execution_count': self.execution_count,
                    'ename': '', 'evalue': str(exitcode), 'traceback': []}
        else:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payloads': [], 'user_expressions': {}}

        def do_shutdown(self, restart):
                self.gdlwrapper.child.kill(signal.SIGKILL)
                return {'status':'ok', 'restart':restart}

if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=GDLKernel)