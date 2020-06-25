#!/bin/tcsh -f
#-------------------------------------------
# qflow exec script for project /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog
#-------------------------------------------

# /usr/local/share/qflow/scripts/yosys.sh /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog/mux_using_if.rtlbb.v || exit 1
# /usr/local/share/qflow/scripts/graywolf.sh -d /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if || exit 1
# /usr/local/share/qflow/scripts/vesta.sh  /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if || exit 1
# /usr/local/share/qflow/scripts/qrouter.sh /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if || exit 1
# /usr/local/share/qflow/scripts/vesta.sh  -d /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if || exit 1
# /usr/local/share/qflow/scripts/magic_db.sh /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if || exit 1
# /usr/local/share/qflow/scripts/magic_drc.sh /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if || exit 1
# /usr/local/share/qflow/scripts/netgen_lvs.sh /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if || exit 1
# /usr/local/share/qflow/scripts/magic_gds.sh /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if || exit 1
# /usr/local/share/qflow/scripts/cleanup.sh /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if || exit 1
# /usr/local/share/qflow/scripts/cleanup.sh -p /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if || exit 1
/usr/local/share/qflow/scripts/magic_view.sh /mnt/data/Code/Internship-2020/asg/test_cases/mux_verilog mux_using_if || exit 1
