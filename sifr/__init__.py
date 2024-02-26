# #############################################################################
# Created by Alexander Ross
# 2nd July 2022
# Version 0.4.1
# #############################################################################
# Sifr is the main script which calculates the main arithmetic of the
# generalised number system.
# It's purpose is not efficiency, but rather to break down mathematical
# processes to its component functions and generalizability.
# This file contains the code to instantiated a Sifr number whilst importing
# SifrSystem class to define the system in which it operates.
# As a general rule the signing of the Sifr is dealt with within the dunder
# method in this file, all other items (xcimal points, recursion for operation
# etc.) are calculated in the SifrSystem object imported.
# #############################################################################

__author__ = "Alexander Ross <alex@ross.vip>"
__version__ = "0.4.1"
___date__ = "22 February 2024"

from sifr.systems import SifrSystem
from sifr.sifr import Sifr
from sifr.xuarizm import Xuarizm
