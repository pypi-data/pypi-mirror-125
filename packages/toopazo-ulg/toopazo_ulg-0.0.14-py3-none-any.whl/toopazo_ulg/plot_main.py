#!/usr/bin/env python

from toopazo_tools.file_folder import FileFolderTools as FFTools
# from toopazo_tools.statistics import TimeseriesStats

from toopazo_ulg.file_parser import UlgParser
from toopazo_ulg.plot_basics import UlgPlotBasics
from toopazo_ulg.plot_sysid import UlgPlotSysid
from toopazo_ulg.plot_mixer import UlgPlotMixer

import os
import argparse
# import sys
# import subprocess
# import csv
# import matplotlib.pyplot as plt


class UlgMain:
    def __init__(self, bdir, pos_vel, att_rates, manctrl, mixer, twin):
        # bdir = FFTools.full_path(args.bdir)
        # bdir = os.path.abspath(args.bdir)
        self.logdir = bdir + '/logs'
        self.tmpdir = bdir + '/tmp'
        self.plotdir = bdir + '/plots'

        try:
            if not os.path.isdir(self.logdir):
                os.mkdir(self.logdir)
            if not os.path.isdir(self.tmpdir):
                os.mkdir(self.logdir)
            if not os.path.isdir(self.plotdir):
                os.mkdir(self.logdir)
        except OSError:
            raise RuntimeError('Directories are not present and could not be created')

        self.pos_vel = pos_vel
        self.att_rates = att_rates
        self.manctrl = manctrl
        self.mixer = mixer
        self.twin = twin

        self.ulg_plot_basics = UlgPlotBasics(
            self.logdir, self.tmpdir, self.plotdir)

        self.ulg_plot_sysid = UlgPlotSysid(
            self.logdir, self.tmpdir, self.plotdir)

        self.ulg_plot_mixer = UlgPlotMixer(
            self.logdir, self.tmpdir, self.plotdir)

        # Remove all files from tmpdir
        # self.ulgparser.clear_tmpdir()

    def check_ulog2csv(self, ulgfile):

        # Check if we need to run ulog2csv
        csvname = 'actuator_controls_0_0'
        csvfile = UlgParser.get_csvfile(self.tmpdir, ulgfile, csvname)
        # if FFTools.is_file(csvfile):
        if os.path.isfile(csvfile):
            # UlgParser.ulog2info(ulgfile)
            pass
        else:
            UlgParser.ulog2csv(ulgfile, self.tmpdir)
            UlgParser.write_vehicle_attitude_0_deg(ulgfile, self.tmpdir)

    def process_file(self, ulgfile):

        print('[process_file] processing %s' % ulgfile)

        self.check_ulog2csv(ulgfile)

        closefig = True

        tmpdir = self.tmpdir
        ulgfile = ulgfile
        csvname = 'vehicle_local_position_0'
        df = UlgParser.get_pandas_dataframe_from_csv_file(tmpdir, ulgfile, csvname)
        print(df)
        return

        if self.pos_vel:
            self.ulg_plot_basics.vehicle_local_position_0(ulgfile, closefig)

        if self.att_rates:
            self.ulg_plot_basics.vehicle_rates_setpoint_0(ulgfile, closefig)
            self.ulg_plot_basics.vehicle_attitude_0_deg(ulgfile, closefig)

        if self.manctrl:
            self.ulg_plot_basics.manual_control_setpoint_0(ulgfile, closefig)

        # self.ulg_plot_basics.nwindow_hover_pos(ulgfile, closefig)
        # self.ulg_plot_basics.nwindow_hover_vel(ulgfile, closefig)

        # self.ulg_plot_sysid.cmd_roll_to_attitude(ulgfile, closefig)
        # self.ulg_plot_sysid.cmd_pitch_to_attitude(ulgfile, closefig)
        # self.ulg_plot_sysid.cmd_yawrate_to_attitude(ulgfile, closefig)
        # self.ulg_plot_sysid.cmd_az_to_attitude(ulgfile, closefig)

        if self.mixer:
            # self.ulg_plot_mixer.mixer_input_output(ulgfile, closefig)
            # self.ulg_plot_basics.actuator_controls_0_0(ulgfile, closefig)
            # self.ulg_plot_basics.actuator_outputs_0(ulgfile, closefig)
            self.ulg_plot_mixer.actuator_controls_0_0(ulgfile, closefig)
            self.ulg_plot_mixer.actuator_outputs_0(ulgfile, closefig)
        # exit(0)

        # plt.show()
        # plt.close()

    def process_logdir(self):
        print('[process_logdir] processing %s' % self.logdir)

        # foldername, extension, method
        FFTools.run_method_on_folder(self.logdir, '.ulg', ulg_data.process_file)


print('[plot_main] module name is %s' % __name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse, process and plot .ulg files')
    parser.add_argument('--bdir', action='store', required=True,
                        help='Base directory of [logs, tmp, plots] folders')
    # parser.add_argument('--plot', action='store_true', required=False,
    #                     help='plot results')
    parser.add_argument('--pos_vel', action='store_true', help='pos and vel')
    parser.add_argument('--att_rates', action='store_true', help='attitude and angular rates')
    parser.add_argument('--manctrl', action='store_true', help='manual control')
    parser.add_argument('--mixer', action='store_true', help='mixer and actuators')
    parser.add_argument('--twin', action='store', help='desired time window', default=None)

    args = parser.parse_args()

    ulg_data = UlgMain(
        os.path.abspath(args.bdir), args.pos_vel, args.att_rates, args.manctrl, args.mixer, args.twin
    )
    ulg_data.process_logdir()

    # Run it as a package
    # python -m toopazo_ulg.plot_main --bdir . --pos_vel --att_rates
