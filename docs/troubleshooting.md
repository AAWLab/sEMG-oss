# Troubleshooting

## Flat Line

Check:

- `OUT` is connected to the ADC pin used in the sketch.
- `GND` is shared between the sEMG module and microcontroller.
- The module is powered correctly.
- Electrodes are connected and making skin contact.
- The selected Teleplot serial port is correct.

## Clipping Or Saturation

If the waveform sticks near the ADC minimum or maximum:

- Check that the module output range fits the ADC range.
- Try wet electrodes to reduce contact impedance.
- Check for loose electrode leads.
- Move away from noisy power supplies or computers.

## Strong 50/60 Hz Noise

Check:

- Electrode contact quality.
- Long or asymmetric input wires.
- Nearby chargers, desktop PCs, monitors, and power adapters.
- Whether the setup is powered from a noisy USB source.

Try battery power and move the setup away from the computer.

## Waveform Changes When Touching Wires

This usually means the input is picking up environmental noise or a connection is loose.

- Fix or shorten loose wires.
- Use stable electrode mounting.
- Avoid hand-pressing electrodes during measurement.
- Keep electrode leads still during the test.
