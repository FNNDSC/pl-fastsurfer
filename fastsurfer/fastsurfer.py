#!/usr/bin/env python                                            
#
# fastsurfer ds ChRIS plugin app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
sys.path.append(os.path.dirname(__file__))

# import the Chris app superclass
from chrisapp.base import ChrisApp


Gstr_title = """

Generate a title from 
http://patorjk.com/software/taag/#p=display&f=Doom&t=fastsurfer

"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       fastsurfer.py 

    SYNOPSIS

        python fastsurfer.py                               \\
            [-h] [--help]                                  \\
            [--json]                                       \\
            [--man]                                        \\
            [--meta]                                       \\
            [--savejson <DIR>]                             \\
            [-v <level>] [--verbosity <level>]             \\
            [--version]                                    \\
            [--fs_license <fs_license>]                    \\
            [--sid <sid>]                                  \\
            [--sd <sd>]                                    \\
            [--t1 <t1>]                                    \\
            [--seg <seg>]                                  \\
            [--seg_log <seg_log>]                          \\
            [--weights_sag <weights_sag>]                  \\
            [--weights_ax <weights_ax>]                    \\
            [--weights_cor <weights_cor>]                  \\
            [--clean_seg <clean_seg>]                      \\
            [--no_cuda <no_cuda>]                          \\
            [--batch <batch>]                              \\
            [--order <order>]                              \\
            [--seg_only <seg_only>]                        \\
            [--seg_with_cc_only <seg_with_cc_only>]        \\
            [--surf_only <surf_only>]                      \\
            [--vol_segstats <vol_segstats>]                \\
            [--fstess <fstess>]                            \\
            [--fsqsphere <fsqsphere>]                      \\
            [--fsaparc <fsaparc>]                          \\
            [--surfreg <surfreg>]                          \\
            [--parallel <parallel>]                        \\
            [--threads <threads>]                          \\
            [--py <py>]                                    \\
            [--fs_help <fs_help>]                          \\
            <inputDir>                                     \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir in out && chmod 777 out
            python fastsurfer.py   \\
                                in    out

    DESCRIPTION

        `fastsurfer.py` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit.

        [--fs_license]
        Path to FreeSurfer license key file. Register (for free) at https://surfer.nmr.mgh.harvard.edu/registration.html to obtain it if you do not have FreeSurfer installed so far.

        [--sid]
        Subject ID for directory inside \$SUBJECTS_DIR to be created.

        [--sd]
        Output directory \$SUBJECTS_DIR (pass via environment or here).

        [--t1]
        T1 full head input (not bias corrected).

        [--seg]
        Name of intermediate DL-based segmentation file (similar to aparc+aseg). Requires an ABSOLUTE Path! Default location: \$SUBJECTS_DIR/\$sid/mri/aparc.DKTatlas+aseg.deep.mgz.

        [--seg_log]
        Log-file for the segmentation (FastSurferCNN). Default: \$SUBJECTS_DIR/\$sid/scripts/deep-seg.log

        [--weights_sag]
        Pretrained weights of sagittal network. Default: ../checkpoints/Sagittal_Weights_FastSurferCNN/ckpts/Epoch_30_training_state.pkl

        [--weights_ax]
        Pretrained weights of axial network. Default: ../checkpoints/Axial_Weights_FastSurferCNN/ckpts/Epoch_30_training_state.pkl

        [--weights_cor]
        Pretrained weights of coronal network. Default: ../checkpoints/Coronal_Weights_FastSurferCNN/ckpts/Epoch_30_training_state.pkl

        [--clean_seg]
        Flag to clean up FastSurferCNN segmentation.

        [--no_cuda]
        Flag to disable CUDA usage in FastSurferCNN (no GPU usage, inference on CPU).

        [--batch]
        Batch size for inference. Default: 8.

        [--order]
        Order of interpolation for mri_convert T1 before segmentation (0=nearest,1=linear(default),2=quadratic,3=cubic)

        [--seg_only]
        Run only FastSurferCNN (generate segmentation, do not run surface pipeline)

        [--seg_with_cc_only]
        Run FastSurferCNN (generate segmentation) and recon_surf until corpus callosum (CC) is added in (no surface models will be created in this case!)

        [--surf_only]
        Run surface pipeline only. The segmentation input has to exist already in this case.

        [--vol_segstats]
        Additionally return volume-based aparc.DKTatlas+aseg statistics for DL-based segmentation (does not require surfaces). Can be used in combination with --seg_only in which case recon-surf only runs till CC is added (akin to --seg_with_cc_only).

        [--fstess]
        Switch on mri_tesselate for surface creation (default: mri_mc)

        [--fsqsphere]
        Use FreeSurfer iterative inflation for qsphere (default: spectral spherical projection)

        [--fsaparc]
        Additionally create FS aparc segmentations and ribbon. Skipped by default (--> DL prediction is used which is faster, and usually these mapped ones are fine)

        [--surfreg]
        Run Surface registration with FreeSurfer (for cross-subject correspondence)

        [--parallel]
        Run both hemispheres in parallel

        [--threads]
        Set openMP and ITK threads to <int>Name of sample weights tensor for loss

        [--py]
        Command for python, default python3.6

        [--fs_help]
        Print FastSurfer help

"""


class Fastsurfer(ChrisApp):
    """
    a fast and accurate deep-learning based neuroimaging pipeline.
    """
    AUTHORS                 = 'Sandip Samal, Grace (sandip.samal@childrens.harvard.edu)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A ChRIS plug-in built around FastSurfer application'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'a fast and accurate deep-learning based neuroimaging pipeline'
    DOCUMENTATION           = 'https://deep-mi.org/research/fastsurfer/'
    VERSION                 = '0.1'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('--fs_license', 
                          dest      = 'fs_license', 
                          type      = str,
                          optional  = True, 
                          help      = 'Path to FreeSurfer license key file. Register (for free) at https://surfer.nmr.mgh.harvard.edu/registration.html to obtain it if you do not have FreeSurfer installed so far.',
                          default   = 'none')

        self.add_argument('--sid',
                          dest      = 'sid',
                          type      = str,
                          optional  = False,
                          help      = 'Subject ID for directory inside \$SUBJECTS_DIR to be created.',
                          default   = 'none')

        self.add_argument('--sd',
                          dest      = 'sd',
                          type      = str,
                          optional  = False,
                          help      = 'Output directory \$SUBJECTS_DIR (pass via environment or here).',
                          default   = 'none')

        self.add_argument('--t1',
                          dest      = 't1',
                          type      = str,
                          optional  = False,
                          help      = 'T1 full head input (not bias corrected).',
                          default   = 'none')

        self.add_argument('--seg',
                          dest      = 'seg',
                          type      = str,
                          optional  = True,
                          help      = 'Name of intermediate DL-based segmentation file (similar to aparc+aseg). Requires an ABSOLUTE Path! Default location: \$SUBJECTS_DIR/\$sid/mri/aparc.DKTatlas+aseg.deep.mgz.',
                          default   = 'none')

        self.add_argument('--seg_log',
                          dest      = 'seg_log',
                          type      = str,
                          optional  = True,
                          help      = 'Log-file for the segmentation (FastSurferCNN). Default: \$SUBJECTS_DIR/\$sid/scripts/deep-seg.log',
                          default   = 'none')

        self.add_argument('--weights_sag',
                          dest      = 'weights_sag',
                          type      = str,
                          optional  = True,
                          help      = 'Pretrained weights of sagittal network. Default: ../checkpoints/Sagittal_Weights_FastSurferCNN/ckpts/Epoch_30_training_state.pkl',
                          default   = 'none')

        self.add_argument('--weights_ax',
                          dest      = 'weights_ax',
                          type      = str,
                          optional  = True,
                          help      = 'Pretrained weights of axial network. Default: ../checkpoints/Axial_Weights_FastSurferCNN/ckpts/Epoch_30_training_state.pkl',
                          default   = 'none')

        self.add_argument('--weights_cor',
                          dest      = 'weights_cor',
                          type      = str,
                          optional  = True,
                          help      = 'Pretrained weights of coronal network. Default: ../checkpoints/Coronal_Weights_FastSurferCNN/ckpts/Epoch_30_training_state.pkl',
                          default   = 'none')

        self.add_argument('--clean_seg',
                          dest      = 'clean_seg',
                          type      = str,
                          optional  = True,
                          help      = 'Flag to clean up FastSurferCNN segmentation.',
                          default   = 'none')

        self.add_argument('--no_cuda',
                          dest      = 'no_cuda',
                          type      = str,
                          optional  = True,
                          help      = 'Flag to disable CUDA usage in FastSurferCNN (no GPU usage, inference on CPU).',
                          default   = 'none')

        self.add_argument('--batch',
                          dest      = 'batch',
                          type      = str,
                          optional  = True,
                          help      = 'Batch size for inference. Default: 8.',
                          default   = 'none')

        self.add_argument('--order',
                          dest      = 'order',
                          type      = str,
                          optional  = True,
                          help      = 'Order of interpolation for mri_convert T1 before segmentation (0=nearest,1=linear(default),2=quadratic,3=cubic)',
                          default   = 'none')

        self.add_argument('--seg_only',
                          dest      = 'seg_only',
                          type      = str,
                          optional  = True,
                          help      = 'Run only FastSurferCNN (generate segmentation, do not run surface pipeline)',
                          default   = 'none')

        self.add_argument('--seg_with_cc_only',
                          dest      = 'seg_with_cc_only',
                          type      = str,
                          optional  = True,
                          help      = 'Run FastSurferCNN (generate segmentation) and recon_surf until corpus callosum (CC) is added in (no surface models will be created in this case!)',
                          default   = 'none')

        self.add_argument('--surf_only',
                          dest      = 'surf_only',
                          type      = str,
                          optional  = True,
                          help      = 'Run surface pipeline only. The segmentation input has to exist already in this case.',
                          default   = 'none')

        self.add_argument('--vol_segstats',
                          dest      = 'vol_segstats',
                          type      = str,
                          optional  = True,
                          help      = 'Additionally return volume-based aparc.DKTatlas+aseg statistics for DL-based segmentation (does not require surfaces). Can be used in combination with --seg_only in which case recon-surf only runs till CC is added (akin to --seg_with_cc_only).',
                          default   = 'none')

        self.add_argument('--fstess',
                          dest      = 'fstess',
                          type      = str,
                          optional  = True,
                          help      = 'Switch on mri_tesselate for surface creation (default: mri_mc)',
                          default   = 'none')

        self.add_argument('--fsqsphere',
                          dest      = 'fsqsphere',
                          type      = str,
                          optional  = True,
                          help      = 'Use FreeSurfer iterative inflation for qsphere (default: spectral spherical projection)',
                          default   = 'none')

        self.add_argument('--fsaparc',
                          dest      = 'fsaparc',
                          type      = str,
                          optional  = True,
                          help      = 'Additionally create FS aparc segmentations and ribbon. Skipped by default (--> DL prediction is used which is faster, and usually these mapped ones are fine)',
                          default   = 'none')

        self.add_argument('--surfreg',
                          dest      = 'surfreg',
                          type      = str,
                          optional  = True,
                          help      = 'Run Surface registration with FreeSurfer (for cross-subject correspondence)',
                          default   = 'none')

        self.add_argument('--parallel',
                          dest      = 'parallel',
                          type      = str,
                          optional  = True,
                          help      = 'Run both hemispheres in parallel',
                          default   = 'none')

        self.add_argument('--threads',
                          dest      = 'threads',
                          type      = str,
                          optional  = True,
                          help      = 'Set openMP and ITK threads to <int>Name of sample weights tensor for loss',
                          default   = 'none')

        self.add_argument('--py',
                          dest      = 'py',
                          type      = str,
                          optional  = True,
                          help      = 'Command for python, default python3.6',
                          default   = 'none')
        
        self.add_argument('--fs_help',
                          dest      = 'fs_help',
                          type      = str,
                          optional  = True,
                          help      = 'Print FastSurfer help',
                          default   = 'none')

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        # dirs: 
        # fastsurfer_dir: /usr/src/fastsurfer/FastSurfer
        fastsurfer_dir = os.path.join(os.getcwd(), 'FastSurfer')

        #print("os.chdir")
        os.chdir(fastsurfer_dir)
        
        fastsurfer_args = {'fs_license', 'sid', 'sd', 't1', 'seg', 'seg_log', 'weights_sag', 'weights_ax', 'weights_cor',
                'clean_seg', 'no_cuda', 'batch', 'order', 'seg_only', 'seg_with_cc_only', 'surf_only', 'vol_segstats',
                'fstess', 'fsqsphere', 'fsaparc', 'surfreg', 'parallel', 'threads', 'py', 'fs_help'}
        
        #print("options:")
        run_fastsurfer_cmd = './run_fastsurfer.sh '
        for option in fastsurfer_args:
            if options.__dict__['fs_help'] is not 'none':
                run_fastsurfer_cmd = run_fastsurfer_cmd + '--help'
                break
            elif options.__dict__[option] is not 'none':
                run_fastsurfer_cmd = run_fastsurfer_cmd + '--' + str(option) + ' ' + str(options.__dict__[option]) + ' '

        #print('final command: ')
        #print(run_fastsurfer_cmd)
        os.system(run_fastsurfer_cmd)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Fastsurfer()
    chris_app.launch()
