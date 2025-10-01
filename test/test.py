# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # ----------------------------------------------------------
    # Test 1: Load value 50 into counter
    dut.ui_in.value = 50
    dut.uio_in.value = 0b101  # load=1, output_enable=1
    await ClockCycles(dut.clk, 1)

    # release load
    dut.uio_in.value = 0b100  # only output_enable=1
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 50, f"Expected 50, got {int(dut.uo_out.value)}"

    # ----------------------------------------------------------
    # Test 2: Enable counting for 5 cycles
    dut.uio_in.value = 0b110  # count_enable=1, output_enable=1
    await ClockCycles(dut.clk, 5)

    expected = 50 + 4 # increment on rising edges expected to be 54
    assert dut.uo_out.value == expected, f"Expected {expected}, got {int(dut.uo_out.value)}"

    # ----------------------------------------------------------
    # Test 3: Disable output
    dut.uio_in.value = 0b010  # count_enable=1, output_enable=0
    await ClockCycles(dut.clk, 1)

    # uo_out should be Z
    out_str = str(dut.uo_out.value)
    assert "z" in out_str.lower(), f"Expected high-Z, got {out_str}"

    # ----------------------------------------------------------
    # Test 4: Re-enable output, should show the correct count
    dut.uio_in.value = 0b110  # count_enable=1, output_enable=1
    await ClockCycles(dut.clk, 1)

    current = int(dut.uo_out.value)
    dut._log.info(f"Counter resumed output at {current}")
    assert current == expected + 2, f"Expected {expected+1}, got {current}"

    dut._log.info("All counter tests passed")
