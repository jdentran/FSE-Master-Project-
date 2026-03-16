SeperaTee — Automatic Laundry Sorter
About / Motivation

SeperaTee is a prototype automatic laundry sorting system designed to help visually impaired individuals separate clothing by color.

This project was developed by me for an engineering class. The system uses an RGB color sensor and servo motors controlled by a Raspberry Pi to detect the color of clothing and automatically sort items into different bins.

The goal is to make the process of separating laundry easier and more accessible using simple electronics and Python.

How It Works

A piece of clothing is placed into the dropper mechanism.

The TCS34725 RGB sensor reads the color of the fabric.

A Python program running on the Raspberry Pi processes the RGB values and classifies the color.

After detection, the dropper releases the clothing onto a sorting platform.

The platform tilts using servo motors depending on the detected color.

The clothing slides into the corresponding bin.

Hardware Used

TCS34725 RGB Color Sensor

MG995 Servo Motors

Raspberry Pi

Jumper Wires

Breadboard

Mechanical dropper mechanism

Tilting sorting platform

Software

Python

Raspberry Pi GPIO libraries

TCS34725 sensor library

The Python script reads RGB values from the sensor and determines which direction the platform should tilt in order to sort the item.

Project Status

This project was developed as a class prototype, so the functionality is experimental and the mechanical design is still rough. The main focus was demonstrating the concept of automated color-based sorting rather than building a fully polished system.
