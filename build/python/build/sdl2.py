import os.path, fileinput, re, shutil, subprocess

from build.autotools import AutotoolsProject

class SDL2Project(AutotoolsProject):
    def configure(self, toolchain, *args, **kwargs):
        if re.match('(arm.*|aarch64)-apple-darwin', toolchain.actual_arch) is not None:
            # for building SDL2 with autotools, several workarounds are
            # required:
            # * out-of-tree build is not supported
            # * needs CFLAGS adjustment to enable Objective-C and ARC
            # * SDL_config.h needs to be replaced with SDL_config_iphoneos.h
            #   after running "configure"

            src = self.unpack(toolchain, out_of_tree=False)

            configure = [
                os.path.join(src, 'configure'),
                'CC=' + toolchain.cc,
                'CFLAGS=' + toolchain.cflags + ' -x objective-c -fobjc-arc',
                'CPPFLAGS=' + toolchain.cppflags + ' ' + self.cppflags,
                'LDFLAGS=' + toolchain.ldflags,
                'LIBS=' + toolchain.libs,
                'AR=' + toolchain.ar,
                'STRIP=' + toolchain.strip,
                '--host=' + toolchain.toolchain_arch,
                '--prefix=' + toolchain.install_prefix,
            ] + self.configure_args

            subprocess.check_call(configure, cwd=src, env=toolchain.env)

            shutil.copyfile(os.path.join(src, 'include/SDL_config_iphoneos.h'),
                            os.path.join(src, 'include/SDL_config.h'))

            return src
        
        if toolchain.actual_arch == 'x86_64-apple-darwin':
            # If an X11 server is installed on macOS then SDL will detect it and
            # enable the X11 video backend. This in turn will lead to XCSoar
            # build errors because SDL_VIDEO_DRIVER_X11 is defined which will
            # lead to a redefinition of a constant. XCSoar does not use X11 on
            # macOS therefore we can disable X11 support.
            self.configure_args += ['--disable-video-x11']

        return AutotoolsProject.configure(self, toolchain)
