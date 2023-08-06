#!/usr/bin/env python3
import csv
import math
import os
import serial
import struct
import time
import typing

"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """''
======================================================================
                    Listas de Entidades BSMP
        A posição da entidade na lista corresponde ao seu ID BSMP
======================================================================
""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
from .utils import get_logger

# common_list
from .constants.common_list import (
    list_ps_models,
    list_common_vars,
    list_curv,
    list_func,
    list_op_mode,
    list_sig_gen_types,
    list_parameters,
)

# fbp_const_list
from .constants.fbp_const_list import (
    list_fbp_soft_interlocks,
    list_fbp_hard_interlocks,
    list_fbp_dclink_hard_interlocks,
)

# fac_const_list
from .constants.fac_const_list import (
    list_fac_acdc_soft_interlocks,
    list_fac_acdc_hard_interlocks,
    list_fac_acdc_iib_is_interlocks,
    list_fac_acdc_iib_is_alarms,
    list_fac_acdc_iib_cmd_interlocks,
    list_fac_acdc_iib_cmd_alarms,
    list_fac_dcdc_soft_interlocks,
    list_fac_dcdc_hard_interlocks,
    list_fac_dcdc_iib_interlocks,
    list_fac_dcdc_iib_alarms,
    list_fac_2s_acdc_soft_interlocks,
    list_fac_2s_acdc_hard_interlocks,
    list_fac_2s_acdc_iib_is_interlocks,
    list_fac_2s_acdc_iib_cmd_interlocks,
    list_fac_2s_acdc_iib_is_alarms,
    list_fac_2s_acdc_iib_cmd_alarms,
    list_fac_2s_dcdc_soft_interlocks,
    list_fac_2s_dcdc_hard_interlocks,
    list_fac_2s_dcdc_iib_interlocks,
    list_fac_2s_dcdc_iib_alarms,
    list_fac_2p4s_dcdc_soft_interlocks,
    list_fac_2p4s_dcdc_hard_interlocks,
    list_fac_2p4s_dcdc_iib_interlocks,
    list_fac_2p4s_dcdc_iib_alarms,
    list_fac_dcdc_ema_soft_interlocks,
    list_fac_dcdc_ema_hard_interlocks,
    list_fac_dcdc_ema_iib_interlocks,
    list_fac_dcdc_ema_iib_alarms,
    list_fac_2p_acdc_imas_soft_interlocks,
    list_fac_2p_acdc_imas_hard_interlocks,
    list_fac_2p_dcdc_imas_soft_interlocks,
    list_fac_2p_dcdc_imas_hard_interlocks,
)

# fap_const_list
from .constants.fap_const_list import (
    list_fap_soft_interlocks,
    list_fap_hard_interlocks,
    list_fap_iib_interlocks,
    list_fap_iib_alarms,
    list_fap_4p_soft_interlocks,
    list_fap_4p_hard_interlocks,
    list_fap_4p_iib_interlocks,
    list_fap_4p_iib_alarms,
    list_fap_2p2s_soft_interlocks,
    list_fap_2p2s_hard_interlocks,
    list_fap_225A_soft_interlocks,
    list_fap_225A_hard_interlocks,
)

UDC_FIRMWARE_VERSION = "0.42 2021-05-06"

type_format = {
    "uint8_t": "BBHBB",
    "uint16_t": "BBHHB",
    "uint32_t": "BBHIB",
    "float": "BBHfB",
}

bytes_format = {"Uint16": "H", "Uint32": "L", "Uint64": "Q", "float": "f"}

type_size = {"uint8_t": 6, "uint16_t": 7, "uint32_t": 9, "float": 9}

num_blocks_curves_fbp = [4, 4, 4]
num_blocks_curves_fax = [16, 16, 16]
size_curve_block = [1024, 1024, 1024]

ufm_offset = {
    "serial": 0,
    "calibdate": 4,
    "variant": 9,
    "rburden": 10,
    "calibtemp": 12,
    "vin_gain": 14,
    "vin_offset": 16,
    "iin_gain": 18,
    "iin_offset": 20,
    "vref_p": 22,
    "vref_n": 24,
    "gnd": 26,
}

hradc_variant = [
    "HRADC-FBP",
    "HRADC-FAX-A",
    "HRADC-FAX-B",
    "HRADC-FAX-C",
    "HRADC-FAX-D",
]

hradc_input_types = [
    "GND",
    "Vref_bipolar_p",
    "Vref_bipolar_n",
    "Temp",
    "Vin_bipolar_p",
    "Vin_bipolar_n",
    "Iin_bipolar_p",
    "Iin_bipolar_n",
]

NUM_MAX_COEFFS_DSP = 12
num_dsp_classes = 7
num_dsp_modules = [4, 4, 4, 6, 8, 4, 2, 2]
num_coeffs_dsp_modules = [0, 1, 1, 4, 8, 16, 2]
dsp_classes_names = [
    "DSP_Error",
    "DSP_SRLim",
    "DSP_LPF",
    "DSP_PI",
    "DSP_IIR_2P2Z",
    "DSP_IIR_3P3Z",
    "DSP_VdcLink_FeedForward",
    "DSP_Vect_Product",
]

logger = get_logger(name=__file__)


class SerialDRS(object):
    def __init__(self):
        # self.ser=serial.Serial()
        self.master_add = "\x00"
        self.slave_add = "\x01"
        self.b_cast_add = "\xFF"
        self.com_write_var = "\x20"
        self.write_float_size_payload = "\x00\x05"
        self.write_double_size_payload = "\x00\x03"
        self.com_read_var = "\x10\x00\x01"
        self.com_request_curve = "\x40"
        self.com_send_wfm_ref = "\x41"
        self.com_function = "\x50"
        self.dp_module_max_coeff = 16

        self.ser: typing.Optional[serial.Serial] = None

        print(
            "\n pyDRS - compatible UDC firmware version: " + UDC_FIRMWARE_VERSION + "\n"
        )

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """''
    ======================================================================
                    Funções Internas da Classe
    ======================================================================
    """ """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
    # Converte float para hexadecimal

    def float_to_hex(self, value):
        hex_value = struct.pack("f", value)
        return hex_value.decode("ISO-8859-1")

    # Converte lista de float  para hexadecimal
    def float_list_to_hex(self, value_list):
        hex_list = b""
        for value in value_list:
            hex_list = hex_list + struct.pack("f", value)
        return hex_list.decode("ISO-8859-1")

    def format_list_size(self, in_list, max_size):
        out_list = in_list[0:max_size]
        if max_size > len(in_list):
            for i in range(max_size - len(in_list)):
                out_list.append(0)
        return out_list

    # Converte double para hexadecimal
    def double_to_hex(self, value):
        hex_value = struct.pack("H", value)
        return hex_value.decode("ISO-8859-1")

    # Converte unsigned int para hexadecimal
    def uint32_to_hex(self, value):
        hex_value = struct.pack("I", value)
        return hex_value.decode("ISO-8859-1")

    # Converte indice para hexadecimal
    def index_to_hex(self, value):
        hex_value = struct.pack("B", value)
        return hex_value.decode("ISO-8859-1")

    # Converte payload_size para hexadecimal
    def size_to_hex(self, value):
        hex_value = struct.pack(">H", value)
        return hex_value.decode("ISO-8859-1")

    # Função Checksum
    def checksum(self, packet):
        b = bytearray(packet.encode("ISO-8859-1"))
        csum = (256 - sum(b)) % 256
        hcsum = struct.pack("B", csum)
        send_msg = packet + hcsum.decode(encoding="ISO-8859-1")
        return send_msg

    # Função de leitura de variável
    def read_var(self, var_id):
        send_msg = self.checksum(self.slave_add + self.com_read_var + var_id)
        self.ser.reset_input_buffer()
        self.ser.write(send_msg.encode("ISO-8859-1"))

    def is_open(self):
        return self.ser.isOpen()

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """''
    ======================================================================
                Métodos de Chamada de Entidades Funções BSMP
            O retorno do método são os bytes de retorno da mensagem
    ======================================================================
    """ """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def turn_on(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("turn_on"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def turn_off(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("turn_off"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def open_loop(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("open_loop"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def closed_loop(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("closed_loop"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def reset_interlocks(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("reset_interlocks"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def read_ps_status(self):
        self.read_var(self.index_to_hex(list_common_vars.index("ps_status")))
        reply_msg = self.ser.read(7)
        val = struct.unpack("BBHHB", reply_msg)
        status = {}
        status["state"] = list_op_mode[(val[3] & 0b0000000000001111)]
        status["open_loop"] = (val[3] & 0b0000000000010000) >> 4
        status["interface"] = (val[3] & 0b0000000001100000) >> 5
        status["active"] = (val[3] & 0b0000000010000000) >> 7
        status["model"] = list_ps_models[(val[3] & 0b0001111100000000) >> 8]
        status["unlocked"] = (val[3] & 0b0010000000000000) >> 13
        # print(status)
        return status

    def set_ps_name(self, ps_name):
        if type(ps_name) == str:
            for n in range(len(ps_name)):
                self.set_param("PS_Name", n, float(ord(ps_name[n])))
            for i in range(n + 1, 64):
                self.set_param("PS_Name", i, float(ord(" ")))

    def get_ps_name(self):
        ps_name = ""
        for n in range(64):
            ps_name = ps_name + chr(int(self.get_param("PS_Name", n)))
            if ps_name[-3:] == "   ":
                ps_name = ps_name[: n - 2]
                break
        return ps_name

    def set_slowref(self, setpoint):
        payload_size = self.size_to_hex(1 + 4)  # Payload: ID + iSlowRef
        hex_setpoint = self.float_to_hex(setpoint)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("set_slowref"))
            + hex_setpoint
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def set_slowref_fbp(self, iRef1=0, iRef2=0, iRef3=0, iRef4=0):
        payload_size = self.size_to_hex(1 + 4 * 4)  # Payload: ID + 4*iRef
        hex_iRef1 = self.float_to_hex(iRef1)
        hex_iRef2 = self.float_to_hex(iRef2)
        hex_iRef3 = self.float_to_hex(iRef3)
        hex_iRef4 = self.float_to_hex(iRef4)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("set_slowref_fbp"))
            + hex_iRef1
            + hex_iRef2
            + hex_iRef3
            + hex_iRef4
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def set_slowref_readback_mon(self, setpoint):
        payload_size = self.size_to_hex(1 + 4)  # Payload: ID + iSlowRef
        hex_setpoint = self.float_to_hex(setpoint)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("set_slowref_readback_mon"))
            + hex_setpoint
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        reply_msg = self.ser.read(9)
        val = struct.unpack("BBHfB", reply_msg)
        return val[3]

    def set_slowref_fbp_readback_mon(self, iRef1=0, iRef2=0, iRef3=0, iRef4=0):
        payload_size = self.size_to_hex(1 + 4 * 4)  # Payload: ID + 4*iRef
        hex_iRef1 = self.float_to_hex(iRef1)
        hex_iRef2 = self.float_to_hex(iRef2)
        hex_iRef3 = self.float_to_hex(iRef3)
        hex_iRef4 = self.float_to_hex(iRef4)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("set_slowref_fbp_readback_mon"))
            + hex_iRef1
            + hex_iRef2
            + hex_iRef3
            + hex_iRef4
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        reply_msg = self.ser.read(21)
        if len(reply_msg) == 6:
            return reply_msg
        else:
            val = struct.unpack("BBHffffB", reply_msg)
            return [val[3], val[4], val[5], val[6]]

    def set_slowref_readback_ref(self, setpoint):
        payload_size = self.size_to_hex(1 + 4)  # Payload: ID + iSlowRef
        hex_setpoint = self.float_to_hex(setpoint)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("set_slowref_readback_ref"))
            + hex_setpoint
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        reply_msg = self.ser.read(9)
        val = struct.unpack("BBHfB", reply_msg)
        return val[3]

    def set_slowref_fbp_readback_ref(self, iRef1=0, iRef2=0, iRef3=0, iRef4=0):
        payload_size = self.size_to_hex(1 + 4 * 4)  # Payload: ID + 4*iRef
        hex_iRef1 = self.float_to_hex(iRef1)
        hex_iRef2 = self.float_to_hex(iRef2)
        hex_iRef3 = self.float_to_hex(iRef3)
        hex_iRef4 = self.float_to_hex(iRef4)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("set_slowref_fbp_readback_ref"))
            + hex_iRef1
            + hex_iRef2
            + hex_iRef3
            + hex_iRef4
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        reply_msg = self.ser.read(21)
        if len(reply_msg) == 6:
            return reply_msg
        else:
            val = struct.unpack("BBHffffB", reply_msg)
            return [val[3], val[4], val[5], val[6]]

    def set_param(self, param_id, n, value):
        payload_size = self.size_to_hex(
            1 + 2 + 2 + 4
        )  # Payload: ID + param id + [n] + value
        if type(param_id) == str:
            hex_id = self.double_to_hex(list_parameters.index(param_id))
        if type(param_id) == int:
            hex_id = self.double_to_hex(param_id)
        hex_n = self.double_to_hex(n)
        hex_value = self.float_to_hex(value)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("set_param"))
            + hex_id
            + hex_n
            + hex_value
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        reply_msg = self.ser.read(6)
        if reply_msg[4] == 8:
            print("Invalid parameter")
        return reply_msg

    def get_param(self, param_id, n=0):
        # Payload: ID + param id + [n]
        payload_size = self.size_to_hex(1 + 2 + 2)
        if type(param_id) == str:
            hex_id = self.double_to_hex(list_parameters.index(param_id))
        if type(param_id) == int:
            hex_id = self.double_to_hex(param_id)
        hex_n = self.double_to_hex(n)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("get_param"))
            + hex_id
            + hex_n
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.reset_input_buffer()
        self.ser.write(send_msg.encode("ISO-8859-1"))
        reply_msg = self.ser.read(9)
        if len(reply_msg) == 9:
            val = struct.unpack("BBHfB", reply_msg)
            return val[3]
        else:
            # print('Invalid parameter')
            return float("nan")

    def save_param_eeprom(self, param_id, n=0, type_memory=2):
        payload_size = self.size_to_hex(
            1 + 2 + 2 + 2
        )  # Payload: ID + param id + [n] + memory type
        if type(param_id) == str:
            hex_id = self.double_to_hex(list_parameters.index(param_id))
        if type(param_id) == int:
            hex_id = self.double_to_hex(param_id)
        hex_n = self.double_to_hex(n)
        hex_type = self.double_to_hex(type_memory)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("save_param_eeprom"))
            + hex_id
            + hex_n
            + hex_type
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        reply_msg = self.ser.read(6)
        if reply_msg[4] == 8:
            print("Invalid parameter")
        return reply_msg

    def load_param_eeprom(self, param_id, n=0, type_memory=2):
        payload_size = self.size_to_hex(
            1 + 2 + 2 + 2
        )  # Payload: ID + param id + [n] + memory type
        if type(param_id) == str:
            hex_id = self.double_to_hex(list_parameters.index(param_id))
        if type(param_id) == int:
            hex_id = self.double_to_hex(param_id)
        hex_n = self.double_to_hex(n)
        hex_type = self.double_to_hex(type_memory)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("load_param_eeprom"))
            + hex_id
            + hex_n
            + hex_type
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        reply_msg = self.ser.read(6)
        if reply_msg[4] == 8:
            print("Invalid parameter")
        return reply_msg

    def save_param_bank(self, type_memory=2):
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID + memory type
        hex_type = self.double_to_hex(type_memory)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("save_param_bank"))
            + hex_type
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def load_param_bank(self, type_memory=2):
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID + memory type
        hex_type = self.double_to_hex(type_memory)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("load_param_bank"))
            + hex_type
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def set_param_bank(self, param_file):
        fbp_param_list = []
        with open(param_file, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                fbp_param_list.append(row)

        for param in fbp_param_list:
            if str(param[0]) == "PS_Name":
                print(str(param[0]) + "[0]: " + str(param[1]))
                print(self.set_ps_name(str(param[1])))
            else:
                for n in range(64):
                    try:
                        print(str(param[0]) + "[" + str(n) + "]: " + str(param[n + 1]))
                        print(self.set_param(str(param[0]), n, float(param[n + 1])))
                    except:
                        break
        # self.save_param_bank()

    def get_param_bank(
        self, list_param=list_parameters, timeout=0.5, print_modules=True
    ):
        timeout_old = self.ser.timeout
        # self.ser.timeout = 0.05
        param_bank = []

        for param_name in list_param:

            param_row = [param_name]

            for n in range(64):
                if param_name == "PS_Name":

                    p = self.get_ps_name()
                    param_row.append(p)
                    # if(print_modules):
                    # print('PS_Name: ' + p)
                    self.ser.timeout = timeout
                    break

                else:
                    p = self.get_param(param_name, n)
                    if math.isnan(p):
                        break
                    param_row.append(p)
                    # if(print_modules):
                    # print(param_name + "[" + str(n) + "]: " + str(p))

            if print_modules:
                print(param_row)

            param_bank.append(param_row)

        self.ser.timeout = timeout_old

        return param_bank

    def store_param_bank_csv(self, bank):
        filename = input("Digite o nome do arquivo: ")
        with open(filename + ".csv", "w", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            for param_row in bank:
                writer.writerow(param_row)

    def enable_onboard_eeprom(self):
        self.set_param("Enable_Onboard_EEPROM", 0, 0)
        self.save_param_eeprom("Enable_Onboard_EEPROM", 0, 2)

    def disable_onboard_eeprom(self):
        self.set_param("Enable_Onboard_EEPROM", 0, 1)
        self.save_param_eeprom("Enable_Onboard_EEPROM", 0, 2)

    def set_dsp_coeffs(
        self, dsp_class, dsp_id, coeffs_list=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ):
        coeffs_list_full = self.format_list_size(coeffs_list, NUM_MAX_COEFFS_DSP)
        payload_size = self.size_to_hex(1 + 2 + 2 + 4 * NUM_MAX_COEFFS_DSP)
        hex_dsp_class = self.double_to_hex(dsp_class)
        hex_dsp_id = self.double_to_hex(dsp_id)
        hex_coeffs = self.float_list_to_hex(coeffs_list_full)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("set_dsp_coeffs"))
            + hex_dsp_class
            + hex_dsp_id
            + hex_coeffs
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def get_dsp_coeff(self, dsp_class, dsp_id, coeff):
        payload_size = self.size_to_hex(1 + 2 + 2 + 2)
        hex_dsp_class = self.double_to_hex(dsp_class)
        hex_dsp_id = self.double_to_hex(dsp_id)
        hex_coeff = self.double_to_hex(coeff)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("get_dsp_coeff"))
            + hex_dsp_class
            + hex_dsp_id
            + hex_coeff
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.reset_input_buffer()
        self.ser.write(send_msg.encode("ISO-8859-1"))
        reply_msg = self.ser.read(9)
        # print(reply_msg)
        val = struct.unpack("BBHfB", reply_msg)
        return val[3]

    def save_dsp_coeffs_eeprom(self, dsp_class, dsp_id, type_memory=2):
        payload_size = self.size_to_hex(1 + 2 + 2 + 2)
        hex_dsp_class = self.double_to_hex(dsp_class)
        hex_dsp_id = self.double_to_hex(dsp_id)
        hex_type = self.double_to_hex(type_memory)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("save_dsp_coeffs_eeprom"))
            + hex_dsp_class
            + hex_dsp_id
            + hex_type
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def load_dsp_coeffs_eeprom(self, dsp_class, dsp_id, type_memory=2):
        payload_size = self.size_to_hex(1 + 2 + 2 + 2)
        hex_dsp_class = self.double_to_hex(dsp_class)
        hex_dsp_id = self.double_to_hex(dsp_id)
        hex_type = self.double_to_hex(type_memory)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("load_dsp_coeffs_eeprom"))
            + hex_dsp_class
            + hex_dsp_id
            + hex_type
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def save_dsp_modules_eeprom(self, type_memory=2):
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID + memory type
        hex_type = self.double_to_hex(type_memory)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("save_dsp_modules_eeprom"))
            + hex_type
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def load_dsp_modules_eeprom(self, type_memory=2):
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID + memory type
        hex_type = self.double_to_hex(type_memory)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("load_dsp_modules_eeprom"))
            + hex_type
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def reset_udc(self):
        reply = input(
            "\nEste comando realiza o reset do firmware da placa UDC, e por isso, so e executado caso a fonte esteja desligada. \nCaso deseje apenas resetar interlocks, utilize o comando reset_interlocks(). \n\nTem certeza que deseja prosseguir? [Y/N]: "
        )
        if reply == "Y" or reply == "y":
            payload_size = self.size_to_hex(1)  # Payload: ID
            send_packet = (
                self.com_function
                + payload_size
                + self.index_to_hex(list_func.index("reset_udc"))
            )
            send_msg = self.checksum(self.slave_add + send_packet)
            self.ser.write(send_msg.encode("ISO-8859-1"))

    def run_bsmp_func(self, id_func, print_msg=0):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = self.com_function + payload_size + self.index_to_hex(id_func)
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        reply_msg = self.ser.read(6)
        if print_msg:
            print(reply_msg)
        return reply_msg

    def run_bsmp_func_all_ps(
        self, p_func, add_list, arg=None, delay=0.5, print_reply=1
    ):
        old_add = self.get_slave_add()
        for add in add_list:
            self.set_slave_add(add)
            if arg is None:
                r = p_func()
            else:
                r = p_func(arg)
            if print_reply:
                print("\n Add " + str(add))
                print(r)
            time.sleep(delay)
        self.set_slave_add(old_add)

    def cfg_source_scope(self, p_source):
        payload_size = self.size_to_hex(1 + 4)  # Payload: ID + p_source
        hex_op_mode = self.uint32_to_hex(p_source)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("cfg_source_scope"))
            + hex_op_mode
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def cfg_freq_scope(self, freq):
        payload_size = self.size_to_hex(1 + 4)  # Payload: ID + freq
        hex_op_mode = self.float_to_hex(freq)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("cfg_freq_scope"))
            + hex_op_mode
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def cfg_duration_scope(self, duration):
        payload_size = self.size_to_hex(1 + 4)  # Payload: ID + duration
        hex_op_mode = self.float_to_hex(duration)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("cfg_duration_scope"))
            + hex_op_mode
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def enable_scope(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("enable_scope"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def disable_scope(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("disable_scope"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def get_scope_vars(self):
        print("\n### Scope Variables ###\n")
        print("Frequency: " + str((round(self.read_bsmp_variable(25, "float"), 3))))
        print("Duration: " + str((round(self.read_bsmp_variable(26, "float"), 3))))
        print(
            "Source Data: " + str((round(self.read_bsmp_variable(27, "uint32_t"), 3)))
        )

    def sync_pulse(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("sync_pulse"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def select_op_mode(self, op_mode):
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID + enable
        hex_op_mode = self.double_to_hex(list_op_mode.index(op_mode))
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("select_op_mode"))
            + hex_op_mode
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def set_serial_termination(self, term_enable):
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID + enable
        hex_enable = self.double_to_hex(term_enable)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("set_serial_termination"))
            + hex_enable
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def set_command_interface(self, interface):
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID + enable
        hex_interface = self.double_to_hex(interface)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("set_command_interface"))
            + hex_interface
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def unlock_udc(self, password):
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID + password
        hex_password = self.double_to_hex(password)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("unlock_udc"))
            + hex_password
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def lock_udc(self, password):
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID + password
        hex_password = self.double_to_hex(password)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("lock_udc"))
            + hex_password
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def reset_counters(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("reset_counters"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def cfg_siggen(
        self, sig_type, num_cycles, freq, amplitude, offset, aux0, aux1, aux2, aux3
    ):
        payload_size = self.size_to_hex(1 + 2 + 2 + 4 + 4 + 4 + 4 * 4)
        hex_sig_type = self.double_to_hex(list_sig_gen_types.index(sig_type))
        hex_num_cycles = self.double_to_hex(num_cycles)
        hex_freq = self.float_to_hex(freq)
        hex_amplitude = self.float_to_hex(amplitude)
        hex_offset = self.float_to_hex(offset)
        hex_aux0 = self.float_to_hex(aux0)
        hex_aux1 = self.float_to_hex(aux1)
        hex_aux2 = self.float_to_hex(aux2)
        hex_aux3 = self.float_to_hex(aux3)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("cfg_siggen"))
            + hex_sig_type
            + hex_num_cycles
            + hex_freq
            + hex_amplitude
            + hex_offset
            + hex_aux0
            + hex_aux1
            + hex_aux2
            + hex_aux3
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def set_siggen(self, freq, amplitude, offset):
        payload_size = self.size_to_hex(1 + 4 + 4 + 4)
        hex_freq = self.float_to_hex(freq)
        hex_amplitude = self.float_to_hex(amplitude)
        hex_offset = self.float_to_hex(offset)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("set_siggen"))
            + hex_freq
            + hex_amplitude
            + hex_offset
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def enable_siggen(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("enable_siggen"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def disable_siggen(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("disable_siggen"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def cfg_wfmref(self, idx, sync_mode, frequency, gain=1, offset=0):
        payload_size = self.size_to_hex(
            1 + 2 + 2 + 4 + 4 + 4
        )  # Payload: ID + idx + sync_mode + frequency + gain + offset
        hex_idx = self.double_to_hex(idx)
        hex_mode = self.double_to_hex(sync_mode)
        hex_freq = self.float_to_hex(frequency)
        hex_gain = self.float_to_hex(gain)
        hex_offset = self.float_to_hex(offset)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("cfg_wfmref"))
            + hex_idx
            + hex_mode
            + hex_freq
            + hex_gain
            + hex_offset
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def select_wfmref(self, idx):
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID + idx
        hex_idx = self.double_to_hex(idx)
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("select_wfmref"))
            + hex_idx
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def reset_wfmref(self):
        payload_size = self.size_to_hex(1)  # Payload: ID
        send_packet = (
            self.com_function
            + payload_size
            + self.index_to_hex(list_func.index("reset_wfmref"))
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(6)

    def get_wfmref_vars(self, curve_id):
        print("\n### WfmRef " + str(curve_id) + " Variables ###\n")
        print(
            "Length: "
            + str(
                (
                    round(self.read_bsmp_variable(20 + curve_id * 3, "uint32_t"), 3)
                    - round(self.read_bsmp_variable(19 + curve_id * 3, "uint32_t"), 3)
                )
                / 2
                + 1
            )
        )
        print(
            "Index: "
            + str(
                (
                    round(self.read_bsmp_variable(21 + curve_id * 3, "uint32_t"), 3)
                    - round(self.read_bsmp_variable(19 + curve_id * 3, "uint32_t"), 3)
                )
                / 2
                + 1
            )
        )
        print(
            "WfmRef Selected: " + str(round(self.read_bsmp_variable(14, "uint16_t"), 3))
        )
        print("Sync Mode: " + str(round(self.read_bsmp_variable(15, "uint16_t"), 3)))
        print(
            "Frequency: " + str(round(self.read_bsmp_variable(16, "float"), 3)) + " Hz"
        )
        print("Gain: " + str(round(self.read_bsmp_variable(17, "float"), 3)))
        print("Offset: " + str(round(self.read_bsmp_variable(18, "float"), 3)))

    def read_csv_file(self, filename, type="float"):
        csv_list = []
        with open(filename, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if type == "float":
                    row_converted = float(row[0])
                elif type == "string" or type == "str":
                    row_converted = str(row[0])
                csv_list.append(row_converted)
        print("Length of list: " + str(len(csv_list)) + "\n")
        return csv_list

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """''
    ======================================================================
                Métodos de Leitura de Valores das Variáveis BSMP
    O retorno do método são os valores double/float da respectiva variavel
    ======================================================================
    """ """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def read_bsmp_variable(self, id_var, type_var, print_msg=0):
        self.read_var(self.index_to_hex(id_var))
        reply_msg = self.ser.read(type_size[type_var])
        if print_msg:
            print(reply_msg)
        val = struct.unpack(type_format[type_var], reply_msg)
        return val[3]

    def read_bsmp_variable_gen(self, id_var, size_bytes, print_msg=0):
        self.read_var(self.index_to_hex(id_var))
        reply_msg = self.ser.read(size_bytes + 5)
        if print_msg:
            print(reply_msg)
        return reply_msg

    def read_udc_arm_version(self):
        self.read_var(self.index_to_hex(3))
        reply_msg = self.ser.read(133)
        val = struct.unpack("16s", reply_msg[4:20])
        return val[0].decode("utf-8")

    def read_udc_c28_version(self):
        self.read_var(self.index_to_hex(3))
        reply_msg = self.ser.read(133)
        val = struct.unpack("16s", reply_msg[20:36])
        return val[0].decode("utf-8")

    def read_udc_version(self):
        print("\n ARM: " + self.read_udc_arm_version())
        print(" C28: " + self.read_udc_c28_version())

    def read_ps_model(self):
        reply_msg = self.read_ps_model()
        return list_ps_models[reply_msg[3]]

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """''
    ======================================================================
                Métodos de Escrita de Valores das Variáveis BSMP
            O retorno do método são os bytes de retorno da mensagem
    ======================================================================
    """ """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def Write_sigGen_Freq(self, float_value):
        hex_float = self.float_to_hex(float_value)
        send_packet = (
            self.com_write_var
            + self.write_float_size_payload
            + self.index_to_hex(list_common_vars.index("sigGen_Freq"))
            + hex_float
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(5)

    def Write_sigGen_Amplitude(self, float_value):
        hex_float = self.float_to_hex(float_value)
        send_packet = (
            self.com_write_var
            + self.write_float_size_payload
            + self.index_to_hex(list_common_vars.index("sigGen_Amplitude"))
            + hex_float
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(5)

    def Write_sigGen_Offset(self, float_value):
        hex_float = self.float_to_hex(float_value)
        send_packet = (
            self.com_write_var
            + self.write_float_size_payload
            + self.index_to_hex(list_common_vars.index("sigGen_Offset"))
            + hex_float
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(5)

    def Write_sigGen_Aux(self, float_value):
        hex_float = self.float_to_hex(float_value)
        send_packet = (
            self.com_write_var
            + self.write_float_size_payload
            + self.index_to_hex(list_common_vars.index("sigGen_Aux"))
            + hex_float
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(5)

    def Write_dp_ID(self, double_value):
        hex_double = self.double_to_hex(double_value)
        send_packet = (
            self.com_write_var
            + self.write_double_size_payload
            + self.index_to_hex(list_common_vars.index("dp_ID"))
            + hex_double
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(5)

    def Write_dp_Class(self, double_value):
        hex_double = self.double_to_hex(double_value)
        send_packet = (
            self.com_write_var
            + self.write_double_size_payload
            + self.index_to_hex(list_common_vars.index("dp_Class"))
            + hex_double
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(5)

    def Write_dp_Coeffs(self, list_float):

        hex_float_list = []
        # list_full = list_float[:]

        # while(len(list_full) < self.dp_module_max_coeff):
        #    list_full.append(0)

        list_full = [0 for i in range(self.dp_module_max_coeff)]
        list_full[: len(list_float)] = list_float[:]

        for float_value in list_full:
            hex_float = self.float_to_hex(float(float_value))
            hex_float_list.append(hex_float)
        str_float_list = "".join(hex_float_list)
        payload_size = self.size_to_hex(
            1 + 4 * self.dp_module_max_coeff
        )  # Payload: ID + 16floats
        send_packet = (
            self.com_write_var
            + payload_size
            + self.index_to_hex(list_common_vars.index("dp_Coeffs"))
            + str_float_list
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(5)

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """''
    ======================================================================
                     Métodos de Escrita de Curvas BSMP
            O retorno do método são os bytes de retorno da mensagem
    ======================================================================
    """ """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def send_wfmref_curve(self, block_idx, data):
        block_hex = struct.pack(">H", block_idx).decode("ISO-8859-1")
        val = []
        for k in range(0, len(data)):
            val.append(self.float_to_hex(float(data[k])))
        payload_size = struct.pack(">H", (len(val) * 4) + 3).decode("ISO-8859-1")
        curva_hex = "".join(val)
        send_packet = (
            self.com_send_wfm_ref
            + payload_size
            + self.index_to_hex(list_curv.index("wfmRef_Curve"))
            + block_hex
            + curva_hex
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(5)

    def recv_wfmref_curve(self, block_idx):
        block_hex = struct.pack(">H", block_idx).decode("ISO-8859-1")
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID+Block_index
        send_packet = (
            self.com_request_curve
            + payload_size
            + self.index_to_hex(list_curv.index("wfmRef_Curve"))
            + block_hex
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        recv_msg = self.ser.read(
            1 + 1 + 2 + 1 + 2 + 8192 + 1
        )  # Address+Command+Size+ID+Block_idx+data+checksum
        val = []
        for k in range(7, len(recv_msg) - 1, 4):
            val.append(struct.unpack("f", recv_msg[k : k + 4]))
        return val

    def recv_samples_buffer(self):
        block_hex = struct.pack(">H", 0).decode("ISO-8859-1")
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID+Block_index
        send_packet = (
            self.com_request_curve
            + payload_size
            + self.index_to_hex(list_curv.index("samplesBuffer"))
            + block_hex
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        recv_msg = self.ser.read(
            1 + 1 + 2 + 1 + 2 + 16384 + 1
        )  # Address+Command+Size+ID+Block_idx+data+checksum
        val = []
        try:
            for k in range(7, len(recv_msg) - 1, 4):
                val.extend(struct.unpack("f", recv_msg[k : k + 4]))
        except:
            pass
        return val

    def send_full_wfmref_curve(self, block_idx, data):
        block_hex = struct.pack(">H", block_idx).decode("ISO-8859-1")
        val = []
        for k in range(0, len(data)):
            val.append(self.float_to_hex(float(data[k])))
        payload_size = struct.pack(">H", (len(val) * 4) + 3).decode("ISO-8859-1")
        curva_hex = "".join(val)
        send_packet = (
            self.com_send_wfm_ref
            + payload_size
            + self.index_to_hex(list_curv.index("fullwfmRef_Curve"))
            + block_hex
            + curva_hex
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(5)

    def recv_full_wfmref_curve(self, block_idx):
        block_hex = struct.pack(">H", block_idx).decode("ISO-8859-1")
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID+Block_index
        send_packet = (
            self.com_request_curve
            + payload_size
            + self.index_to_hex(list_curv.index("fullwfmRef_Curve"))
            + block_hex
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        recv_msg = self.ser.read(
            1 + 1 + 2 + 1 + 2 + 16384 + 1
        )  # Address+Command+Size+ID+Block_idx+data+checksum
        val = []
        for k in range(7, len(recv_msg) - 1, 4):
            val.append(struct.unpack("f", recv_msg[k : k + 4]))
        return val

    def recv_samples_buffer_blocks(self, block_idx):
        block_hex = struct.pack(">H", block_idx).decode("ISO-8859-1")
        payload_size = self.size_to_hex(1 + 2)  # Payload: ID+Block_index
        send_packet = (
            self.com_request_curve
            + payload_size
            + self.index_to_hex(list_curv.index("samplesBuffer_blocks"))
            + block_hex
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        # t0 = time.time()
        self.ser.write(send_msg.encode("ISO-8859-1"))
        recv_msg = self.ser.read(
            1 + 1 + 2 + 1 + 2 + 1024 + 1
        )  # Address+Command+Size+ID+Block_idx+data+checksum
        # print(time.time()-t0)
        # print(recv_msg)
        val = []
        for k in range(7, len(recv_msg) - 1, 4):
            val.extend(struct.unpack("f", recv_msg[k : k + 4]))
        return val

    def recv_samples_buffer_allblocks(self):
        buff = []
        # self.DisableSamplesBuffer()
        for i in range(0, 16):
            # t0 = time.time()
            buff.extend(self.recv_samples_buffer_blocks(i))
            # print(time.time()-t0)
        # self.EnableSamplesBuffer()
        return buff

    def read_curve_block(self, curve_id, block_id):
        block_hex = struct.pack(">H", block_id).decode("ISO-8859-1")
        payload_size = self.size_to_hex(1 + 2)  # Payload: curve_id + block_id
        send_packet = (
            self.com_request_curve
            + payload_size
            + self.index_to_hex(curve_id)
            + block_hex
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        # t0 = time.time()
        self.ser.reset_input_buffer()
        self.ser.write(send_msg.encode("ISO-8859-1"))
        recv_msg = self.ser.read(
            1 + 1 + 2 + 1 + 2 + size_curve_block[curve_id] + 1
        )  # Address+Command+Size+ID+Block_idx+data+checksum
        # print(time.time()-t0)
        # print(recv_msg)
        val = []
        for k in range(7, len(recv_msg) - 1, 4):
            val.extend(struct.unpack("f", recv_msg[k : k + 4]))
        return val

    def write_curve_block(self, curve_id, block_id, data):
        block_hex = struct.pack(">H", block_id).decode("ISO-8859-1")
        val = []
        for k in range(0, len(data)):
            val.append(self.float_to_hex(float(data[k])))
        payload_size = struct.pack(">H", (len(val) * 4) + 3).decode("ISO-8859-1")
        curva_hex = "".join(val)
        send_packet = (
            self.com_send_wfm_ref
            + payload_size
            + self.index_to_hex(curve_id)
            + block_hex
            + curva_hex
        )
        send_msg = self.checksum(self.slave_add + send_packet)
        self.ser.write(send_msg.encode("ISO-8859-1"))
        return self.ser.read(5)

    def write_wfmref(self, curve, data):
        # curve = list_curv.index('wfmref')
        block_size = int(size_curve_block[curve] / 4)
        print(block_size)

        blocks = [data[x : x + block_size] for x in range(0, len(data), block_size)]

        ps_status = self.read_ps_status()

        wfmref_selected = self.read_bsmp_variable(14, "uint16_t")

        if (wfmref_selected == curve) and (
            ps_status["state"] == "RmpWfm" or ps_status["state"] == "MigWfm"
        ):
            print(
                "\n The specified curve ID is currently selected and PS is on "
                + ps_status["state"]
                + " state. Choose a different curve ID to proceed.\n"
            )

        else:
            for block_id in range(len(blocks)):
                self.write_curve_block(curve, block_id, blocks[block_id])
                print(blocks[block_id])

    def read_buf_samples_ctom(self):
        buf = []
        curve_id = list_curv.index("buf_samples_ctom")

        ps_status = self.read_ps_status()
        if ps_status["model"] == "FBP":
            for i in range(num_blocks_curves_fbp[curve_id]):
                buf.extend(self.read_curve_block(curve_id, i))
        else:
            for i in range(num_blocks_curves_fax[curve_id]):
                buf.extend(self.read_curve_block(curve_id, i))

        return buf

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """''
    ======================================================================
                            Funções Serial
    ======================================================================
    """ """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def connect(self, port="COM2", baud=115200):
        if self.ser and self.ser.is_open:
            logger.warning(
                "PyDRS obj {} serial port {} is already open settings. Disconnect before opening a new connection.".format(
                    self, self.ser
                )
            )
            return False
        try:
            self.ser = serial.Serial(
                port, baud, timeout=1
            )  # port format should be 'COM'+number
            return True
        except Exception:
            # Do not use bare `except:`, it also catches unexpected events like memory errors, interrupts, system exit, and so on.  Prefer `except Exception:`.
            # If you're sure what you're doing, be explicit and write `except BaseException:`

            # logger.exception will display the stacktrace, useful debugging tool
            logger.exception("Failed to open serial port ({}, {})".format(port, baud))
            return False

    def disconnect(self):
        if not self.ser or not self.ser.is_open:
            # Early return if already closed
            return True

        try:
            self.ser.close()
            return True
        except Exception:
            # Do not use bare `except:`, it also catches unexpected events like memory errors, interrupts, system exit, and so on.  Prefer `except Exception:`.
            # If you're sure what you're doing, be explicit and write `except BaseException:`

            # logger.exception will display the stacktrace, useful debugging tool
            logger.exception("Failed to disconnect serial port ({})".format(self.ser))
            return False

    def set_slave_add(self, address):
        self.slave_add = struct.pack("B", address).decode("ISO-8859-1")

    def get_slave_add(self):
        return struct.unpack("B", self.slave_add.encode())[0]

    """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """''
    ======================================================================
                      Funções auxiliares
    ======================================================================
    """ """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

    def read_vars_common(self, print_all=False):

        loop_state = ["Closed Loop", "Open Loop"]

        ps_status = self.read_ps_status()
        if ps_status["open_loop"] == 0:
            if (
                (ps_status["model"] == "FAC_ACDC")
                or (ps_status["model"] == "FAC_2S_ACDC")
                or (ps_status["model"] == "FAC_2P4S_ACDC")
            ):
                setpoint_unit = " V"
            else:
                setpoint_unit = " A"
        else:
            setpoint_unit = " %"

        print("\nPS Model: " + ps_status["model"])
        print("State: " + ps_status["state"])
        print("Loop State: " + loop_state[ps_status["open_loop"]])

        print(
            "\nSetpoint: "
            + str(round(self.read_bsmp_variable(1, "float"), 3))
            + setpoint_unit
        )
        print(
            "Reference: "
            + str(round(self.read_bsmp_variable(2, "float"), 3))
            + setpoint_unit
        )

        if print_all:
            print(self.read_ps_status())

            print(
                "\nCounter set_slowref: "
                + str(round(self.read_bsmp_variable(4, "uint32_t"), 3))
            )
            print(
                "Counter sync pulse: "
                + str(round(self.read_bsmp_variable(5, "uint32_t"), 3))
            )

            self.get_siggen_vars()
            self.get_wfmref_vars(0)
            self.get_wfmref_vars(1)
            self.get_scope_vars()

    def _interlock_unknown_assignment(self, active_interlocks, index):
        active_interlocks.append("bit {}: Reserved".format(index))

    def _interlock_name_assigned(self, active_interlocks, index, list_interlocks):
        active_interlocks.append("bit {}: {}".format(index, list_interlocks[index]))

    def decode_interlocks(self, reg_interlocks, list_interlocks):
        active_interlocks = []
        for index in range(32):
            if reg_interlocks & (1 << index):
                if index < len(list_interlocks):
                    self._interlock_name_assigned(
                        active_interlocks, index, list_interlocks
                    )
                else:
                    self._interlock_unknown_assignment(active_interlocks, index)

        for interlock in active_interlocks:
            print(interlock)
        return active_interlocks

    def read_vars_fbp(self, n=1, dt=0.5):

        try:
            for i in range(n):

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )
                self.read_vars_common()

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(soft_itlks, list_fbp_soft_interlocks)
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(hard_itlks, list_fbp_hard_interlocks)

                print(
                    "\nLoad Current: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                    + " A"
                )
                print(
                    "Load Voltage: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " V"
                )
                print(
                    "Load Resistance: "
                    + str(
                        abs(
                            round(
                                self.read_bsmp_variable(34, "float")
                                / self.read_bsmp_variable(33, "float"),
                                3,
                            )
                        )
                    )
                    + " Ohm"
                )
                print(
                    "Load Power: "
                    + str(
                        abs(
                            round(
                                self.read_bsmp_variable(34, "float")
                                * self.read_bsmp_variable(33, "float"),
                                3,
                            )
                        )
                    )
                    + " W"
                )
                print(
                    "DC-Link Voltage: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " V"
                )
                print(
                    "Heat-Sink Temp: "
                    + str(round(self.read_bsmp_variable(36, "float"), 3))
                    + " °C"
                )
                print(
                    "Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(37, "float"), 3))
                    + " %"
                )

                time.sleep(dt)

        except:
            pass

    def read_vars_fbp_dclink(self, n=1, dt=0.5):

        try:
            for i in range(n):

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )
                self.read_vars_common()

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("\nHard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(hard_itlks, list_fbp_dclink_hard_interlocks)

                print(
                    "\nModules status: "
                    + str(round(self.read_bsmp_variable(33, "uint32_t"), 3))
                )
                print(
                    "DC-Link Voltage: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " V"
                )
                print(
                    "PS1 Voltage: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " V"
                )
                print(
                    "PS2 Voltage: "
                    + str(round(self.read_bsmp_variable(36, "float"), 3))
                    + " V"
                )
                print(
                    "PS3 Voltage: "
                    + str(round(self.read_bsmp_variable(37, "float"), 3))
                    + " V"
                )
                print(
                    "Dig Pot Tap: "
                    + str(round(self.read_bsmp_variable(38, "uint8_t"), 3))
                )

                time.sleep(dt)

        except:
            pass

    def read_vars_fac_acdc(self, n=1, dt=0.5, iib=1):

        # try:
        for i in range(n):

            print(
                "\n--- Measurement #"
                + str(i + 1)
                + " ------------------------------------------\n"
            )
            self.read_vars_common()

            soft_itlks = self.read_bsmp_variable(31, "uint32_t")
            print("\nSoft Interlocks: " + str(soft_itlks))
            if soft_itlks:
                self.decode_interlocks(soft_itlks, list_fac_acdc_soft_interlocks)
                print("")

            hard_itlks = self.read_bsmp_variable(32, "uint32_t")
            print("Hard Interlocks: " + str(hard_itlks))
            if hard_itlks:
                self.decode_interlocks(hard_itlks, list_fac_acdc_hard_interlocks)

            iib_is_itlks = self.read_bsmp_variable(45, "uint32_t")
            print("\nIIB IS Interlocks: " + str(iib_is_itlks))
            if iib_is_itlks:
                self.decode_interlocks(iib_is_itlks, list_fac_acdc_iib_is_interlocks)

            iib_is_alarms = self.read_bsmp_variable(46, "uint32_t")
            print("IIB IS Alarms: " + str(iib_is_alarms))
            if iib_is_alarms:
                self.decode_interlocks(iib_is_alarms, list_fac_acdc_iib_is_alarms)

            iib_cmd_itlks = self.read_bsmp_variable(57, "uint32_t")
            print("\nIIB Cmd Interlocks: " + str(iib_cmd_itlks))
            if iib_cmd_itlks:
                self.decode_interlocks(iib_cmd_itlks, list_fac_acdc_iib_cmd_interlocks)

            iib_cmd_alarms = self.read_bsmp_variable(58, "uint32_t")
            print("IIB Cmd Alarms: " + str(iib_cmd_alarms))
            if iib_cmd_alarms:
                self.decode_interlocks(iib_cmd_alarms, list_fac_acdc_iib_cmd_alarms)

            print(
                "\nCapBank Voltage: "
                + str(round(self.read_bsmp_variable(33, "float"), 3))
                + " V"
            )
            print(
                "Rectifier Current: "
                + str(round(self.read_bsmp_variable(34, "float"), 3))
                + " A"
            )

            print(
                "Duty-Cycle: "
                + str(round(self.read_bsmp_variable(35, "float"), 3))
                + " %"
            )

            if iib:
                print(
                    "\nIIB IS Input Current: "
                    + str(round(self.read_bsmp_variable(36, "float"), 3))
                    + " A"
                )
                print(
                    "IIB IS Input Voltage: "
                    + str(round(self.read_bsmp_variable(37, "float"), 3))
                    + " V"
                )
                print(
                    "IIB IS IGBT Temp: "
                    + str(round(self.read_bsmp_variable(38, "float"), 3))
                    + " °C"
                )
                print(
                    "IIB IS Driver Voltage: "
                    + str(round(self.read_bsmp_variable(39, "float"), 3))
                    + " V"
                )
                print(
                    "IIB IS Driver Current: "
                    + str(round(self.read_bsmp_variable(40, "float"), 3))
                    + " A"
                )
                print(
                    "IIB IS Inductor Temp: "
                    + str(round(self.read_bsmp_variable(41, "float"), 3))
                    + " °C"
                )
                print(
                    "IIB IS Heat-Sink Temp: "
                    + str(round(self.read_bsmp_variable(42, "float"), 3))
                    + " °C"
                )
                print(
                    "IIB IS Board Temp: "
                    + str(round(self.read_bsmp_variable(43, "float"), 3))
                    + " °C"
                )
                print(
                    "IIB IS Board RH: "
                    + str(round(self.read_bsmp_variable(44, "float"), 3))
                    + " %"
                )
                print(
                    "IIB IS Interlocks: "
                    + str(round(self.read_bsmp_variable(45, "uint32_t"), 3))
                )
                print(
                    "IIB IS Alarms: "
                    + str(round(self.read_bsmp_variable(46, "uint32_t"), 3))
                )

                print(
                    "\nIIB Cmd Load Voltage: "
                    + str(round(self.read_bsmp_variable(47, "float"), 3))
                    + " V"
                )
                print(
                    "IIB Cmd CapBank Voltage: "
                    + str(round(self.read_bsmp_variable(48, "float"), 3))
                    + " V"
                )
                print(
                    "IIB Cmd Rectifier Inductor Temp: "
                    + str(round(self.read_bsmp_variable(49, "float"), 3))
                    + " °C"
                )
                print(
                    "IIB Cmd Rectifier Heat-Sink Temp: "
                    + str(round(self.read_bsmp_variable(50, "float"), 3))
                    + " °C"
                )
                print(
                    "IIB Cmd External Boards Voltage: "
                    + str(round(self.read_bsmp_variable(51, "float"), 3))
                    + " V"
                )
                print(
                    "IIB Cmd Auxiliary Board Current: "
                    + str(round(self.read_bsmp_variable(52, "float"), 3))
                    + " A"
                )
                print(
                    "IIB Cmd IDB Board Current: "
                    + str(round(self.read_bsmp_variable(53, "float"), 3))
                    + " A"
                )
                print(
                    "IIB Cmd Ground Leakage Current: "
                    + str(round(self.read_bsmp_variable(54, "float"), 3))
                    + " A"
                )
                print(
                    "IIB Cmd Board Temp: "
                    + str(round(self.read_bsmp_variable(55, "float"), 3))
                    + " °C"
                )
                print(
                    "IIB Cmd Board RH: "
                    + str(round(self.read_bsmp_variable(56, "float"), 3))
                    + " %"
                )
                print(
                    "IIB Cmd Interlocks: "
                    + str(round(self.read_bsmp_variable(57, "uint32_t"), 3))
                )
                print(
                    "IIB Cmd Alarms: "
                    + str(round(self.read_bsmp_variable(58, "uint32_t"), 3))
                )

            time.sleep(dt)

        # except:
        #    pass

    def read_vars_fac_dcdc(self, n=1, dt=0.5, iib=1):

        try:
            for i in range(n):

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )
                self.read_vars_common()

                print(
                    "\nSync Pulse Counter: "
                    + str(round(self.read_bsmp_variable(5, "uint32_t"), 3))
                )
                print(
                    "WfmRef Index: "
                    + str(
                        (
                            round(self.read_bsmp_variable(20, "uint32_t"), 3)
                            - round(self.read_bsmp_variable(18, "uint32_t"), 3)
                        )
                        / 2
                        + 1
                    )
                )

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(soft_itlks, list_fac_dcdc_soft_interlocks)
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(hard_itlks, list_fac_dcdc_hard_interlocks)

                iib_itlks = self.read_bsmp_variable(51, "uint32_t")
                print("\nIIB Interlocks: " + str(iib_itlks))
                if iib_itlks:
                    self.decode_interlocks(iib_itlks, list_fac_dcdc_iib_interlocks)

                iib_alarms = self.read_bsmp_variable(52, "uint32_t")
                print("IIB Alarms: " + str(iib_alarms))
                if iib_alarms:
                    self.decode_interlocks(iib_alarms, list_fac_dcdc_iib_alarms)

                print(
                    "\nLoad Current: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                    + " A"
                )
                print(
                    "Load Current DCCT 1: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " A"
                )
                print(
                    "Load Current DCCT 2: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " A"
                )

                print(
                    "\nCapBank Voltage: "
                    + str(round(self.read_bsmp_variable(36, "float"), 3))
                    + " V"
                )

                print(
                    "\nDuty-Cycle: "
                    + str(round(self.read_bsmp_variable(37, "float"), 3))
                    + " %"
                )

                if iib:
                    print(
                        "\nIIB CapBank Voltage: "
                        + str(round(self.read_bsmp_variable(38, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Input Current: "
                        + str(round(self.read_bsmp_variable(39, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Output Current: "
                        + str(round(self.read_bsmp_variable(40, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB IGBT Leg 1 Temp: "
                        + str(round(self.read_bsmp_variable(41, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IGBT Leg 2 Temp: "
                        + str(round(self.read_bsmp_variable(42, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Inductor Temp: "
                        + str(round(self.read_bsmp_variable(43, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Heat-Sink Temp: "
                        + str(round(self.read_bsmp_variable(44, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Driver Voltage: "
                        + str(round(self.read_bsmp_variable(45, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Driver Current 1: "
                        + str(round(self.read_bsmp_variable(46, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Driver Current 2: "
                        + str(round(self.read_bsmp_variable(47, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Ground Leakage Current: "
                        + str(round(self.read_bsmp_variable(48, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Board Temp: "
                        + str(round(self.read_bsmp_variable(49, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Board RH: "
                        + str(round(self.read_bsmp_variable(50, "float"), 3))
                        + " %"
                    )
                    print(
                        "IIB Interlocks: "
                        + str(round(self.read_bsmp_variable(51, "uint32_t"), 3))
                    )
                    print(
                        "IIB Alarms: "
                        + str(round(self.read_bsmp_variable(52, "uint32_t"), 3))
                    )

                time.sleep(dt)

        except:
            pass

    def read_vars_fac_dcdc_ema(self, n=1, dt=0.5, iib=0):

        try:
            for i in range(n):

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )
                self.read_vars_common()

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(
                        soft_itlks, list_fac_dcdc_ema_soft_interlocks
                    )
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(
                        hard_itlks, list_fac_dcdc_ema_hard_interlocks
                    )

                iib_itlks = self.read_bsmp_variable(49, "uint32_t")
                print("IIB Interlocks: " + str(iib_itlks))
                if iib_itlks:
                    self.decode_interlocks(iib_itlks, list_fac_dcdc_ema_iib_interlocks)

                iib_alarms = self.read_bsmp_variable(50, "uint32_t")
                print("IIB Alarms: " + str(iib_alarms))
                if iib_alarms:
                    self.decode_interlocks(iib_alarms, list_fac_dcdc_ema_iib_alarms)

                print(
                    "\nLoad Current: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                )
                print(
                    "DC-Link Voltage: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                )
                print(
                    "\nDuty-Cycle: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                )

                if iib:
                    print(
                        "\nIIB Input Voltage: "
                        + str(round(self.read_bsmp_variable(36, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Input Current: "
                        + str(round(self.read_bsmp_variable(37, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Output Current: "
                        + str(round(self.read_bsmp_variable(38, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB IGBT 1 Temp: "
                        + str(round(self.read_bsmp_variable(39, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IGBT 2 Temp: "
                        + str(round(self.read_bsmp_variable(40, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Inductor Temp: "
                        + str(round(self.read_bsmp_variable(41, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Heat-Sink Temp: "
                        + str(round(self.read_bsmp_variable(42, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Driver Voltage: "
                        + str(round(self.read_bsmp_variable(43, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Driver Current 1: "
                        + str(round(self.read_bsmp_variable(44, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Driver Current 2: "
                        + str(round(self.read_bsmp_variable(45, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Ground Leakage Current: "
                        + str(round(self.read_bsmp_variable(46, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Board Temp: "
                        + str(round(self.read_bsmp_variable(47, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Board RH: "
                        + str(round(self.read_bsmp_variable(48, "float"), 3))
                        + " %"
                    )
                    print(
                        "IIB Interlocks: "
                        + str(round(self.read_bsmp_variable(49, "uint32_t"), 3))
                    )
                    print(
                        "IIB Alarms: "
                        + str(round(self.read_bsmp_variable(50, "uint32_t"), 3))
                    )

                time.sleep(dt)

        except:
            pass

    def read_vars_fac_2s_acdc(self, n=1, add_mod_a=2, dt=0.5, iib=0):

        old_add = self.get_slave_add()

        try:
            for i in range(n):

                self.set_slave_add(add_mod_a)

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )
                self.read_vars_common()

                print("\n *** MODULE A ***")

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(soft_itlks, list_fac_2s_acdc_soft_interlocks)
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(hard_itlks, list_fac_2s_acdc_hard_interlocks)

                iib_is_itlks = self.read_bsmp_variable(45, "uint32_t")
                print("\nIIB IS Interlocks: " + str(iib_is_itlks))
                if iib_is_itlks:
                    self.decode_interlocks(
                        iib_is_itlks, list_fac_2s_acdc_iib_is_interlocks
                    )

                iib_is_alarms = self.read_bsmp_variable(46, "uint32_t")
                print("IIB IS Alarms: " + str(iib_is_alarms))
                if iib_is_alarms:
                    self.decode_interlocks(
                        iib_is_alarms, list_fac_2s_acdc_iib_is_alarms
                    )

                iib_cmd_itlks = self.read_bsmp_variable(57, "uint32_t")
                print("\nIIB Cmd Interlocks: " + str(iib_cmd_itlks))
                if iib_cmd_itlks:
                    self.decode_interlocks(
                        iib_cmd_itlks, list_fac_2s_acdc_iib_cmd_interlocks
                    )

                iib_cmd_alarms = self.read_bsmp_variable(58, "uint32_t")
                print("IIB Cmd Alarms: " + str(iib_cmd_alarms))
                if iib_cmd_alarms:
                    self.decode_interlocks(
                        iib_cmd_alarms, list_fac_2s_acdc_iib_cmd_alarms
                    )

                print(
                    "\nCapBank Voltage: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                    + " V"
                )
                print(
                    "Rectifier Current: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " A"
                )
                print(
                    "Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " %"
                )

                if iib:
                    print(
                        "\nIIB IS Input Current: "
                        + str(round(self.read_bsmp_variable(36, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB IS Input Voltage: "
                        + str(round(self.read_bsmp_variable(37, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB IS IGBT Temp: "
                        + str(round(self.read_bsmp_variable(38, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IS Driver Voltage: "
                        + str(round(self.read_bsmp_variable(39, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB IS Driver Current: "
                        + str(round(self.read_bsmp_variable(40, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB IS Inductor Temp: "
                        + str(round(self.read_bsmp_variable(41, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IS Heat-Sink Temp: "
                        + str(round(self.read_bsmp_variable(42, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IS Board Temp: "
                        + str(round(self.read_bsmp_variable(43, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IS Board RH: "
                        + str(round(self.read_bsmp_variable(44, "float"), 3))
                        + " %"
                    )
                    print(
                        "IIB IS Interlocks: "
                        + str(round(self.read_bsmp_variable(45, "uint32_t"), 3))
                    )
                    print(
                        "IIB IS Alarms: "
                        + str(round(self.read_bsmp_variable(46, "uint32_t"), 3))
                    )

                    print(
                        "\nIIB Cmd Load Voltage: "
                        + str(round(self.read_bsmp_variable(47, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Cmd CapBank Voltage: "
                        + str(round(self.read_bsmp_variable(48, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Cmd Rectifier Inductor Temp: "
                        + str(round(self.read_bsmp_variable(49, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Cmd Rectifier Heat-Sink Temp: "
                        + str(round(self.read_bsmp_variable(50, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Cmd External Boards Voltage: "
                        + str(round(self.read_bsmp_variable(51, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Cmd Auxiliary Board Current: "
                        + str(round(self.read_bsmp_variable(52, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Cmd IDB Board Current: "
                        + str(round(self.read_bsmp_variable(53, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Cmd Ground Leakage Current: "
                        + str(round(self.read_bsmp_variable(54, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Cmd Board Temp: "
                        + str(round(self.read_bsmp_variable(55, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Cmd Board RH: "
                        + str(round(self.read_bsmp_variable(56, "float"), 3))
                        + " %"
                    )
                    print(
                        "IIB Cmd Interlocks: "
                        + str(round(self.read_bsmp_variable(57, "uint32_t"), 3))
                    )
                    print(
                        "IIB Cmd Alarms: "
                        + str(round(self.read_bsmp_variable(58, "uint32_t"), 3))
                    )

                self.set_slave_add(add_mod_a + 1)

                print("\n *** MODULE B ***")

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(soft_itlks, list_fac_2s_acdc_soft_interlocks)
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(hard_itlks, list_fac_2s_acdc_hard_interlocks)

                iib_is_itlks = self.read_bsmp_variable(45, "uint32_t")
                print("\nIIB IS Interlocks: " + str(iib_is_itlks))
                if iib_is_itlks:
                    self.decode_interlocks(
                        iib_is_itlks, list_fac_2s_acdc_iib_is_interlocks
                    )

                iib_is_alarms = self.read_bsmp_variable(46, "uint32_t")
                print("IIB IS Alarms: " + str(iib_is_alarms))
                if iib_is_alarms:
                    self.decode_interlocks(
                        iib_is_alarms, list_fac_2s_acdc_iib_is_alarms
                    )

                iib_cmd_itlks = self.read_bsmp_variable(57, "uint32_t")
                print("\nIIB Cmd Interlocks: " + str(iib_cmd_itlks))
                if iib_cmd_itlks:
                    self.decode_interlocks(
                        iib_cmd_itlks, list_fac_2s_acdc_iib_cmd_interlocks
                    )

                iib_cmd_alarms = self.read_bsmp_variable(58, "uint32_t")
                print("IIB Cmd Alarms: " + str(iib_cmd_alarms))
                if iib_cmd_alarms:
                    self.decode_interlocks(
                        iib_cmd_alarms, list_fac_2s_acdc_iib_cmd_alarms
                    )

                print(
                    "\nCapBank Voltage: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                    + " V"
                )
                print(
                    "Rectifier Current: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " A"
                )
                print(
                    "Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " %"
                )

                if iib:
                    print(
                        "\nIIB IS Input Current: "
                        + str(round(self.read_bsmp_variable(36, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB IS Input Voltage: "
                        + str(round(self.read_bsmp_variable(37, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB IS IGBT Temp: "
                        + str(round(self.read_bsmp_variable(38, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IS Driver Voltage: "
                        + str(round(self.read_bsmp_variable(39, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB IS Driver Current: "
                        + str(round(self.read_bsmp_variable(40, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB IS Inductor Temp: "
                        + str(round(self.read_bsmp_variable(41, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IS Heat-Sink Temp: "
                        + str(round(self.read_bsmp_variable(42, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IS Board Temp: "
                        + str(round(self.read_bsmp_variable(43, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IS Board RH: "
                        + str(round(self.read_bsmp_variable(44, "float"), 3))
                        + " %"
                    )
                    print(
                        "IIB IS Interlocks: "
                        + str(round(self.read_bsmp_variable(45, "uint32_t"), 3))
                    )
                    print(
                        "IIB IS Alarms: "
                        + str(round(self.read_bsmp_variable(46, "uint32_t"), 3))
                    )

                    print(
                        "\nIIB Cmd Load Voltage: "
                        + str(round(self.read_bsmp_variable(47, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Cmd CapBank Voltage: "
                        + str(round(self.read_bsmp_variable(48, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Cmd Rectifier Inductor Temp: "
                        + str(round(self.read_bsmp_variable(49, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Cmd Rectifier Heat-Sink Temp: "
                        + str(round(self.read_bsmp_variable(50, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Cmd External Boards Voltage: "
                        + str(round(self.read_bsmp_variable(51, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Cmd Auxiliary Board Current: "
                        + str(round(self.read_bsmp_variable(52, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Cmd IDB Board Current: "
                        + str(round(self.read_bsmp_variable(53, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Cmd Ground Leakage Current: "
                        + str(round(self.read_bsmp_variable(54, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Cmd Board Temp: "
                        + str(round(self.read_bsmp_variable(55, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Cmd Board RH: "
                        + str(round(self.read_bsmp_variable(56, "float"), 3))
                        + " %"
                    )
                    print(
                        "IIB Cmd Interlocks: "
                        + str(round(self.read_bsmp_variable(57, "uint32_t"), 3))
                    )
                    print(
                        "IIB Cmd Alarms: "
                        + str(round(self.read_bsmp_variable(58, "uint32_t"), 3))
                    )

                time.sleep(dt)

            self.set_slave_add(old_add)
        except:
            self.set_slave_add(old_add)

    def read_vars_fac_2s_dcdc(self, n=1, com_add=1, dt=0.5, iib=0):

        old_add = self.get_slave_add()
        iib_offset = 14 * (iib - 1)

        try:
            for i in range(n):

                self.set_slave_add(com_add)

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )

                self.read_vars_common()

                print(
                    "\nSync Pulse Counter: "
                    + str(round(self.read_bsmp_variable(5, "uint32_t"), 3))
                )

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(soft_itlks, list_fac_2s_dcdc_soft_interlocks)
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(hard_itlks, list_fac_2s_dcdc_hard_interlocks)

                _load_current = round(self.read_bsmp_variable(33, "float"), 3)
                print("\nLoad Current: {} A".format(_load_current))

                _load_current_dcct1 = round(self.read_bsmp_variable(34, "float"), 3)
                print("Load Current DCCT 1: {} A".format(_load_current_dcct1))

                _load_current_dcct2 = round(self.read_bsmp_variable(35, "float"), 3)
                print("Load Current DCCT 2: {} A".format(_load_current_dcct2))

                print(
                    "\nCapBank Voltage 1: "
                    + str(round(self.read_bsmp_variable(36, "float"), 3))
                    + " V"
                )
                print(
                    "CapBank Voltage 2: "
                    + str(round(self.read_bsmp_variable(37, "float"), 3))
                    + " V"
                )

                print(
                    "\nDuty-Cycle 1: "
                    + str(round(self.read_bsmp_variable(38, "float"), 3))
                    + " %"
                )
                print(
                    "Duty-Cycle 2: "
                    + str(round(self.read_bsmp_variable(39, "float"), 3))
                    + " %"
                )

                if iib:
                    print(
                        "\nIIB CapBank Voltage: "
                        + str(
                            round(self.read_bsmp_variable(40 + iib_offset, "float"), 3)
                        )
                        + " V"
                    )
                    print(
                        "IIB Input Current: "
                        + str(
                            round(self.read_bsmp_variable(41 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB Output Current: "
                        + str(
                            round(self.read_bsmp_variable(42 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB IGBT Leg 1 Temp: "
                        + str(
                            round(self.read_bsmp_variable(43 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB IGBT Leg 2 Temp: "
                        + str(
                            round(self.read_bsmp_variable(44 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB Inductor Temp: "
                        + str(
                            round(self.read_bsmp_variable(45 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB Heat-Sink Temp: "
                        + str(
                            round(self.read_bsmp_variable(46 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB Driver Voltage: "
                        + str(
                            round(self.read_bsmp_variable(47 + iib_offset, "float"), 3)
                        )
                        + " V"
                    )
                    print(
                        "IIB Driver Current 1: "
                        + str(
                            round(self.read_bsmp_variable(48 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB Driver Current 2: "
                        + str(
                            round(self.read_bsmp_variable(49 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB Board Temp: "
                        + str(
                            round(self.read_bsmp_variable(50 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB Board RH: "
                        + str(
                            round(self.read_bsmp_variable(51 + iib_offset, "float"), 3)
                        )
                        + " %"
                    )

                    iib_itlks = self.read_bsmp_variable(52 + iib_offset, "uint32_t")
                    print("\nIIB Interlocks: " + str(iib_itlks))
                    if iib_itlks:
                        self.decode_interlocks(
                            iib_itlks, list_fac_2s_dcdc_iib_interlocks
                        )

                    iib_alarms = self.read_bsmp_variable(53 + iib_offset, "uint32_t")
                    print("IIB Alarms: " + str(iib_alarms))
                    if iib_alarms:
                        self.decode_interlocks(iib_alarms, list_fac_2s_dcdc_iib_alarms)

                time.sleep(dt)

            self.set_slave_add(old_add)
        except:
            self.set_slave_add(old_add)

    def read_vars_fac_2p4s_acdc(self, n=1, add_mod_a=1, dt=0.5, iib=0):
        self.read_vars_fac_2s_acdc(n, add_mod_a, dt, iib)

    def read_vars_fac_2p4s_dcdc(self, n=1, com_add=1, dt=0.5, iib=0):

        old_add = self.get_slave_add()

        try:
            for i in range(n):

                self.set_slave_add(com_add)

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )

                self.read_vars_common()

                print(
                    "\nSync Pulse Counter: "
                    + str(round(self.read_bsmp_variable(5, "uint32_t"), 3))
                )

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(
                        soft_itlks, list_fac_2p4s_dcdc_soft_interlocks
                    )
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(
                        hard_itlks, list_fac_2p4s_dcdc_hard_interlocks
                    )

                print(
                    "\nLoad Current: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                )
                print(
                    "Load Current DCCT 1: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                )
                print(
                    "Load Current DCCT 2: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                )

                print(
                    "\nArm Current 1: "
                    + str(round(self.read_bsmp_variable(36, "float"), 3))
                )
                print(
                    "Arm Current 2: "
                    + str(round(self.read_bsmp_variable(37, "float"), 3))
                )

                print(
                    "\nCapBank Voltage 1: "
                    + str(round(self.read_bsmp_variable(38, "float"), 3))
                )
                print(
                    "CapBank Voltage 2: "
                    + str(round(self.read_bsmp_variable(39, "float"), 3))
                )
                print(
                    "CapBank Voltage 3: "
                    + str(round(self.read_bsmp_variable(40, "float"), 3))
                )
                print(
                    "CapBank Voltage 4: "
                    + str(round(self.read_bsmp_variable(41, "float"), 3))
                )
                print(
                    "CapBank Voltage 5: "
                    + str(round(self.read_bsmp_variable(42, "float"), 3))
                )
                print(
                    "CapBank Voltage 6: "
                    + str(round(self.read_bsmp_variable(43, "float"), 3))
                )
                print(
                    "CapBank Voltage 7: "
                    + str(round(self.read_bsmp_variable(44, "float"), 3))
                )
                print(
                    "CapBank Voltage 8: "
                    + str(round(self.read_bsmp_variable(45, "float"), 3))
                )

                print(
                    "\nDuty-Cycle 1: "
                    + str(round(self.read_bsmp_variable(46, "float"), 3))
                )
                print(
                    "Duty-Cycle 2: "
                    + str(round(self.read_bsmp_variable(47, "float"), 3))
                )
                print(
                    "Duty-Cycle 3: "
                    + str(round(self.read_bsmp_variable(48, "float"), 3))
                )
                print(
                    "Duty-Cycle 4: "
                    + str(round(self.read_bsmp_variable(49, "float"), 3))
                )
                print(
                    "Duty-Cycle 5: "
                    + str(round(self.read_bsmp_variable(50, "float"), 3))
                )
                print(
                    "Duty-Cycle 6: "
                    + str(round(self.read_bsmp_variable(51, "float"), 3))
                )
                print(
                    "Duty-Cycle 7: "
                    + str(round(self.read_bsmp_variable(52, "float"), 3))
                )
                print(
                    "Duty-Cycle 8: "
                    + str(round(self.read_bsmp_variable(53, "float"), 3))
                )

                if iib:

                    print(
                        "\nIIB CapBank Voltage: "
                        + str(round(self.read_bsmp_variable(54, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Input Current: "
                        + str(round(self.read_bsmp_variable(55, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Output Current: "
                        + str(round(self.read_bsmp_variable(56, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB IGBT Leg 1 Temp: "
                        + str(round(self.read_bsmp_variable(57, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IGBT Leg 2 Temp: "
                        + str(round(self.read_bsmp_variable(58, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Inductor Temp: "
                        + str(round(self.read_bsmp_variable(59, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Heat-Sink Temp: "
                        + str(round(self.read_bsmp_variable(60, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Driver Voltage: "
                        + str(round(self.read_bsmp_variable(61, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Driver Current 1: "
                        + str(round(self.read_bsmp_variable(62, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Driver Current 2: "
                        + str(round(self.read_bsmp_variable(63, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Board Temp: "
                        + str(round(self.read_bsmp_variable(64, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Board RH: "
                        + str(round(self.read_bsmp_variable(65, "float"), 3))
                        + " %"
                    )

                    iib_itlks = self.read_bsmp_variable(66, "uint32_t")
                    print("\nIIB Interlocks: " + str(iib_itlks))
                    if iib_itlks:
                        self.decode_interlocks(
                            iib_itlks, list_fac_2p4s_dcdc_iib_interlocks
                        )

                    iib_alarms = self.read_bsmp_variable(67, "uint32_t")
                    print("IIB Alarms: " + str(iib_alarms))
                    if iib_alarms:
                        self.decode_interlocks(
                            iib_alarms, list_fac_2p4s_dcdc_iib_alarms
                        )

                    print(
                        "\nIIB CapBank Voltage: "
                        + str(round(self.read_bsmp_variable(68, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Input Current: "
                        + str(round(self.read_bsmp_variable(69, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Output Current: "
                        + str(round(self.read_bsmp_variable(70, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB IGBT Leg 1 Temp: "
                        + str(round(self.read_bsmp_variable(71, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IGBT Leg 2 Temp: "
                        + str(round(self.read_bsmp_variable(72, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Inductor Temp: "
                        + str(round(self.read_bsmp_variable(73, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Heat-Sink Temp: "
                        + str(round(self.read_bsmp_variable(74, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Driver Voltage: "
                        + str(round(self.read_bsmp_variable(75, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Driver Current 1: "
                        + str(round(self.read_bsmp_variable(76, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Driver Current 2: "
                        + str(round(self.read_bsmp_variable(77, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Board Temp: "
                        + str(round(self.read_bsmp_variable(78, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Board RH: "
                        + str(round(self.read_bsmp_variable(79, "float"), 3))
                        + " %"
                    )

                    iib_itlks = self.read_bsmp_variable(80, "uint32_t")
                    print("\nIIB Interlocks: " + str(iib_itlks))
                    if iib_itlks:
                        self.decode_interlocks(
                            iib_itlks, list_fac_2p4s_dcdc_iib_interlocks
                        )

                    iib_alarms = self.read_bsmp_variable(81, "uint32_t")
                    print("IIB Alarms: " + str(iib_alarms))
                    if iib_alarms:
                        self.decode_interlocks(
                            iib_alarms, list_fac_2p4s_dcdc_iib_alarms
                        )

                time.sleep(dt)

            self.set_slave_add(old_add)
        except:
            self.set_slave_add(old_add)

    def read_vars_fap(self, n=1, com_add=1, dt=0.5, iib=1):

        old_add = self.get_slave_add()

        try:
            for i in range(n):

                self.set_slave_add(com_add)

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )
                self.read_vars_common()

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(soft_itlks, list_fap_soft_interlocks)
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(hard_itlks, list_fap_hard_interlocks)

                iib_itlks = self.read_bsmp_variable(56, "uint32_t")
                print("\nIIB Interlocks: " + str(iib_itlks))
                if iib_itlks:
                    self.decode_interlocks(iib_itlks, list_fap_iib_interlocks)

                iib_alarms = self.read_bsmp_variable(57, "uint32_t")
                print("\nIIB Alarms: " + str(iib_alarms))
                if iib_alarms:
                    self.decode_interlocks(iib_alarms, list_fap_iib_alarms)

                iload = self.read_bsmp_variable(33, "float")

                print("\nLoad Current: " + str(round(iload, 3)) + " A")
                print(
                    "Load Current DCCT 1: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " A"
                )
                print(
                    "Load Current DCCT 2: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " A"
                )

                if not iload == 0:
                    print(
                        "\nLoad Resistance: "
                        + str(
                            abs(round(self.read_bsmp_variable(43, "float") / iload, 3))
                        )
                        + " Ohm"
                    )
                else:
                    print("\nLoad Resistance: 0 Ohm")
                print(
                    "Load Power: "
                    + str(
                        abs(
                            round(
                                self.read_bsmp_variable(43, "float")
                                * self.read_bsmp_variable(33, "float"),
                                3,
                            )
                        )
                    )
                    + " W"
                )

                print(
                    "\nDC-Link Voltage: "
                    + str(round(self.read_bsmp_variable(36, "float"), 3))
                    + " V"
                )
                print(
                    "\nIGBT 1 Current: "
                    + str(round(self.read_bsmp_variable(37, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 2 Current: "
                    + str(round(self.read_bsmp_variable(38, "float"), 3))
                    + " A"
                )
                print(
                    "\nIGBT 1 Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(39, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 2 Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(40, "float"), 3))
                    + " %"
                )
                print(
                    "Differential Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(41, "float"), 3))
                    + " %"
                )

                if iib:
                    print(
                        "\nIIB Input Voltage: "
                        + str(round(self.read_bsmp_variable(42, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Output Voltage: "
                        + str(round(self.read_bsmp_variable(43, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB IGBT 1 Current: "
                        + str(round(self.read_bsmp_variable(44, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB IGBT 2 Current: "
                        + str(round(self.read_bsmp_variable(45, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB IGBT 1 Temp: "
                        + str(round(self.read_bsmp_variable(46, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB IGBT 2 Temp: "
                        + str(round(self.read_bsmp_variable(47, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Driver Voltage: "
                        + str(round(self.read_bsmp_variable(48, "float"), 3))
                        + " V"
                    )
                    print(
                        "IIB Driver Current 1: "
                        + str(round(self.read_bsmp_variable(49, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Driver Current 2: "
                        + str(round(self.read_bsmp_variable(50, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Inductor Temp: "
                        + str(round(self.read_bsmp_variable(51, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Heat-Sink Temp: "
                        + str(round(self.read_bsmp_variable(52, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Ground Leakage Current: "
                        + str(round(self.read_bsmp_variable(53, "float"), 3))
                        + " A"
                    )
                    print(
                        "IIB Board Temp: "
                        + str(round(self.read_bsmp_variable(54, "float"), 3))
                        + " °C"
                    )
                    print(
                        "IIB Board RH: "
                        + str(round(self.read_bsmp_variable(55, "float"), 3))
                        + " %"
                    )
                    print(
                        "IIB Interlocks: "
                        + str(round(self.read_bsmp_variable(56, "uint32_t"), 3))
                    )
                    print(
                        "IIB Alarms: "
                        + str(round(self.read_bsmp_variable(57, "uint32_t"), 3))
                    )
                time.sleep(dt)

            self.set_slave_add(old_add)
        except:
            self.set_slave_add(old_add)

    def read_vars_fap_4p(self, n=1, com_add=1, dt=0.5, iib=0):

        old_add = self.get_slave_add()
        iib_offset = 16 * (iib - 1)

        try:
            for i in range(n):

                self.set_slave_add(com_add)

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )
                self.read_vars_common()

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(soft_itlks, list_fap_4p_soft_interlocks)
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(hard_itlks, list_fap_4p_hard_interlocks)

                for j in range(4):
                    iib_itlks = self.read_bsmp_variable(72 + j * 16, "uint32_t")
                    print("\nIIB " + str(j + 1) + " Interlocks: " + str(iib_itlks))
                    if iib_itlks:
                        self.decode_interlocks(iib_itlks, list_fap_4p_iib_interlocks)

                    iib_alarms = self.read_bsmp_variable(73 + j * 16, "uint32_t")
                    print("IIB " + str(j + 1) + " Alarms: " + str(iib_alarms))
                    if iib_alarms:
                        self.decode_interlocks(iib_alarms, list_fap_4p_iib_alarms)

                print(
                    "\n Mean Load Current: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                    + " A"
                )
                print(
                    "Load Current 1: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " A"
                )
                print(
                    "Load Current 2: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " A"
                )

                print(
                    "Load Voltage: "
                    + str(round(self.read_bsmp_variable(36, "float"), 3))
                    + " V"
                )

                print(
                    "\nIGBT 1 Current Mod 1: "
                    + str(round(self.read_bsmp_variable(37, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 2 Current Mod 1: "
                    + str(round(self.read_bsmp_variable(38, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 1 Current Mod 2: "
                    + str(round(self.read_bsmp_variable(39, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 2 Current Mod 2: "
                    + str(round(self.read_bsmp_variable(40, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 1 Current Mod 3: "
                    + str(round(self.read_bsmp_variable(41, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 2 Current Mod 3: "
                    + str(round(self.read_bsmp_variable(42, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 1 Current Mod 4: "
                    + str(round(self.read_bsmp_variable(43, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 2 Current Mod 4: "
                    + str(round(self.read_bsmp_variable(44, "float"), 3))
                    + " A"
                )

                print(
                    "\nDC-Link Voltage Mod 1: "
                    + str(round(self.read_bsmp_variable(45, "float"), 3))
                    + " V"
                )
                print(
                    "DC-Link Voltage Mod 2: "
                    + str(round(self.read_bsmp_variable(46, "float"), 3))
                    + " V"
                )
                print(
                    "DC-Link Voltage Mod 3: "
                    + str(round(self.read_bsmp_variable(47, "float"), 3))
                    + " V"
                )
                print(
                    "DC-Link Voltage Mod 4: "
                    + str(round(self.read_bsmp_variable(48, "float"), 3))
                    + " V"
                )

                print(
                    "\nMean Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(49, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 1 Duty-Cycle Mod 1: "
                    + str(round(self.read_bsmp_variable(50, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 2 Duty-Cycle Mod 1: "
                    + str(round(self.read_bsmp_variable(51, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 1 Duty-Cycle Mod 2: "
                    + str(round(self.read_bsmp_variable(52, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 2 Duty-Cycle Mod 2: "
                    + str(round(self.read_bsmp_variable(53, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 1 Duty-Cycle Mod 3: "
                    + str(round(self.read_bsmp_variable(54, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 2 Duty-Cycle Mod 3: "
                    + str(round(self.read_bsmp_variable(55, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 1 Duty-Cycle Mod 4: "
                    + str(round(self.read_bsmp_variable(56, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 2 Duty-Cycle Mod 4: "
                    + str(round(self.read_bsmp_variable(57, "float"), 3))
                    + " %"
                )

                if not iib == 0:
                    print(
                        "\nIIB "
                        + str(iib)
                        + " Input Voltage: "
                        + str(
                            round(self.read_bsmp_variable(58 + iib_offset, "float"), 3)
                        )
                        + " V"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Output Voltage: "
                        + str(
                            round(self.read_bsmp_variable(59 + iib_offset, "float"), 3)
                        )
                        + " V"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " IGBT 1 Current: "
                        + str(
                            round(self.read_bsmp_variable(60 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " IGBT 2 Current: "
                        + str(
                            round(self.read_bsmp_variable(61 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " IGBT 1 Temp: "
                        + str(
                            round(self.read_bsmp_variable(62 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " IGBT 2 Temp: "
                        + str(
                            round(self.read_bsmp_variable(63 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Driver Voltage: "
                        + str(
                            round(self.read_bsmp_variable(64 + iib_offset, "float"), 3)
                        )
                        + " V"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Driver Current 1: "
                        + str(
                            round(self.read_bsmp_variable(65 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Driver Current 2: "
                        + str(
                            round(self.read_bsmp_variable(66 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Inductor Temp: "
                        + str(
                            round(self.read_bsmp_variable(67 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Heat-Sink Temp: "
                        + str(
                            round(self.read_bsmp_variable(68 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Ground Leakage Current: "
                        + str(
                            round(self.read_bsmp_variable(69 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Board Temp: "
                        + str(
                            round(self.read_bsmp_variable(70 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Board RH: "
                        + str(
                            round(self.read_bsmp_variable(71 + iib_offset, "float"), 3)
                        )
                        + " %"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Interlocks: "
                        + str(
                            round(
                                self.read_bsmp_variable(72 + iib_offset, "uint32_t"), 3
                            )
                        )
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Alarms: "
                        + str(
                            round(
                                self.read_bsmp_variable(73 + iib_offset, "uint32_t"), 3
                            )
                        )
                    )

                time.sleep(dt)

            self.set_slave_add(old_add)

        except Exception as e:
            print(e)
            self.set_slave_add(old_add)

    def read_vars_fap_2p2s(self, n=1, com_add=1, dt=0.5, iib=0):

        old_add = self.get_slave_add()
        iib_offset = 16 * (iib - 1)

        try:
            for i in range(n):

                self.set_slave_add(com_add)

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )
                self.read_vars_common()

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(soft_itlks, list_fap_2p2s_soft_interlocks)
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(hard_itlks, list_fap_2p2s_hard_interlocks)

                for j in range(4):
                    iib_itlks = self.read_bsmp_variable(78 + j * 16, "uint32_t")
                    print("\nIIB " + str(j + 1) + " Interlocks: " + str(iib_itlks))
                    if iib_itlks:
                        self.decode_interlocks(iib_itlks, list_fap_4p_iib_interlocks)

                    iib_alarms = self.read_bsmp_variable(79 + j * 16, "uint32_t")
                    print("IIB " + str(j + 1) + " Alarms: " + str(iib_alarms))
                    if iib_alarms:
                        self.decode_interlocks(iib_alarms, list_fap_4p_iib_alarms)

                print(
                    "\nMean Load Current: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                    + " A"
                )
                print(
                    "Load Current 1: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " A"
                )
                print(
                    "Load Current 2: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " A"
                )

                print(
                    "\nArm Current 1: "
                    + str(round(self.read_bsmp_variable(36, "float"), 3))
                    + " A"
                )
                print(
                    "Arm Current 2: "
                    + str(round(self.read_bsmp_variable(37, "float"), 3))
                    + " A"
                )

                print(
                    "\nIGBT 1 Current Mod 1: "
                    + str(round(self.read_bsmp_variable(38, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 2 Current Mod 1: "
                    + str(round(self.read_bsmp_variable(39, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 1 Current Mod 2: "
                    + str(round(self.read_bsmp_variable(40, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 2 Current Mod 2: "
                    + str(round(self.read_bsmp_variable(41, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 1 Current Mod 3: "
                    + str(round(self.read_bsmp_variable(42, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 2 Current Mod 3: "
                    + str(round(self.read_bsmp_variable(43, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 1 Current Mod 4: "
                    + str(round(self.read_bsmp_variable(44, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 2 Current Mod 4: "
                    + str(round(self.read_bsmp_variable(45, "float"), 3))
                    + " A"
                )

                print(
                    "\nDC-Link Voltage Mod 1: "
                    + str(round(self.read_bsmp_variable(50, "float"), 3))
                    + " V"
                )
                print(
                    "DC-Link Voltage Mod 2: "
                    + str(round(self.read_bsmp_variable(51, "float"), 3))
                    + " V"
                )
                print(
                    "DC-Link Voltage Mod 3: "
                    + str(round(self.read_bsmp_variable(52, "float"), 3))
                    + " V"
                )
                print(
                    "DC-Link Voltage Mod 4: "
                    + str(round(self.read_bsmp_variable(53, "float"), 3))
                    + " V"
                )

                print(
                    "\nMean Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(54, "float"), 3))
                    + " %"
                )
                print(
                    "Differential Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(55, "float"), 3))
                    + " %"
                )
                print(
                    "\nIGBT 1 Duty-Cycle Mod 1: "
                    + str(round(self.read_bsmp_variable(56, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 2 Duty-Cycle Mod 1: "
                    + str(round(self.read_bsmp_variable(57, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 1 Duty-Cycle Mod 2: "
                    + str(round(self.read_bsmp_variable(58, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 2 Duty-Cycle Mod 2: "
                    + str(round(self.read_bsmp_variable(59, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 1 Duty-Cycle Mod 3: "
                    + str(round(self.read_bsmp_variable(60, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 2 Duty-Cycle Mod 3: "
                    + str(round(self.read_bsmp_variable(61, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 1 Duty-Cycle Mod 4: "
                    + str(round(self.read_bsmp_variable(62, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 2 Duty-Cycle Mod 4: "
                    + str(round(self.read_bsmp_variable(63, "float"), 3))
                    + " %"
                )

                if not iib == 0:
                    print(
                        "\nIIB "
                        + str(iib)
                        + " Input Voltage: "
                        + str(
                            round(self.read_bsmp_variable(64 + iib_offset, "float"), 3)
                        )
                        + " V"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Output Voltage: "
                        + str(
                            round(self.read_bsmp_variable(65 + iib_offset, "float"), 3)
                        )
                        + " V"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " IGBT 1 Current: "
                        + str(
                            round(self.read_bsmp_variable(66 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " IGBT 2 Current: "
                        + str(
                            round(self.read_bsmp_variable(67 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " IGBT 1 Temp: "
                        + str(
                            round(self.read_bsmp_variable(68 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " IGBT 2 Temp: "
                        + str(
                            round(self.read_bsmp_variable(69 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Driver Voltage: "
                        + str(
                            round(self.read_bsmp_variable(70 + iib_offset, "float"), 3)
                        )
                        + " V"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Driver Current 1: "
                        + str(
                            round(self.read_bsmp_variable(71 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Driver Current 2: "
                        + str(
                            round(self.read_bsmp_variable(72 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Inductor Temp: "
                        + str(
                            round(self.read_bsmp_variable(73 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Heat-Sink Temp: "
                        + str(
                            round(self.read_bsmp_variable(74 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Ground Leakage Current: "
                        + str(
                            round(self.read_bsmp_variable(75 + iib_offset, "float"), 3)
                        )
                        + " A"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Board Temp: "
                        + str(
                            round(self.read_bsmp_variable(76 + iib_offset, "float"), 3)
                        )
                        + " °C"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Board RH: "
                        + str(
                            round(self.read_bsmp_variable(77 + iib_offset, "float"), 3)
                        )
                        + " %"
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Interlocks: "
                        + str(
                            round(
                                self.read_bsmp_variable(78 + iib_offset, "uint32_t"), 3
                            )
                        )
                    )
                    print(
                        "IIB "
                        + str(iib)
                        + " Alarms: "
                        + str(
                            round(
                                self.read_bsmp_variable(79 + iib_offset, "uint32_t"), 3
                            )
                        )
                    )

                time.sleep(dt)

            self.set_slave_add(old_add)

        except Exception as e:
            print(e)
            self.set_slave_add(old_add)

    def read_vars_fap_225A(self, n=1, com_add=1, dt=0.5):

        old_add = self.get_slave_add()

        try:
            for i in range(n):

                self.set_slave_add(com_add)

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )
                self.read_vars_common()

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(soft_itlks, list_fap_225A_soft_interlocks)
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(hard_itlks, list_fap_225A_hard_interlocks)

                print(
                    "\nLoad Current: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                    + " A"
                )
                print(
                    "\nIGBT 1 Current: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " A"
                )
                print(
                    "IGBT 2 Current: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " A"
                )
                print(
                    "\nIGBT 1 Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(36, "float"), 3))
                    + " %"
                )
                print(
                    "IGBT 2 Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(37, "float"), 3))
                    + " %"
                )
                print(
                    "Differential Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(38, "float"), 3))
                    + " %"
                )

                time.sleep(dt)

            self.set_slave_add(old_add)
        except:
            self.set_slave_add(old_add)

    def read_vars_fac_2p_acdc_imas(self, n=1, add_mod_a=2, dt=0.5, iib=0):

        old_add = self.get_slave_add()

        try:
            for i in range(n):

                self.set_slave_add(add_mod_a)

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )
                self.read_vars_common()

                print("\n *** MODULE A ***")

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(
                        soft_itlks, list_fac_2p_acdc_imas_soft_interlocks
                    )
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(
                        hard_itlks, list_fac_2p_acdc_imas_hard_interlocks
                    )

                print(
                    "\nCapBank Voltage: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                    + " V"
                )
                print(
                    "Rectifier Current: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " A"
                )
                print(
                    "Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " %"
                )

                self.set_slave_add(add_mod_a + 1)

                print("\n *** MODULE B ***")

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(
                        soft_itlks, list_fac_2p_acdc_imas_soft_interlocks
                    )
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(
                        hard_itlks, list_fac_2p_acdc_imas_hard_interlocks
                    )

                print(
                    "\nCapBank Voltage: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                    + " V"
                )
                print(
                    "Rectifier Current: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " A"
                )
                print(
                    "Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " %"
                )

                time.sleep(dt)

            self.set_slave_add(old_add)
        except:
            self.set_slave_add(old_add)
            raise

    def read_vars_fac_2p_dcdc_imas(self, n=1, com_add=1, dt=0.5, iib=0):

        old_add = self.get_slave_add()

        try:
            for i in range(n):

                self.set_slave_add(com_add)

                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )

                self.read_vars_common()

                print(
                    "\nSync Pulse Counter: "
                    + str(round(self.read_bsmp_variable(5, "uint32_t"), 3))
                )

                soft_itlks = self.read_bsmp_variable(31, "uint32_t")
                print("\nSoft Interlocks: " + str(soft_itlks))
                if soft_itlks:
                    self.decode_interlocks(
                        soft_itlks, list_fac_2p_dcdc_imas_soft_interlocks
                    )
                    print("")

                hard_itlks = self.read_bsmp_variable(32, "uint32_t")
                print("Hard Interlocks: " + str(hard_itlks))
                if hard_itlks:
                    self.decode_interlocks(
                        hard_itlks, list_fac_2p_dcdc_imas_hard_interlocks
                    )

                print(
                    "\nLoad Current: "
                    + str(round(self.read_bsmp_variable(33, "float"), 3))
                    + " A"
                )
                print(
                    "Load Current Error: "
                    + str(round(self.read_bsmp_variable(34, "float"), 3))
                    + " A"
                )

                print(
                    "\nArm 1 Current: "
                    + str(round(self.read_bsmp_variable(35, "float"), 3))
                    + " A"
                )
                print(
                    "Arm 2 Current: "
                    + str(round(self.read_bsmp_variable(36, "float"), 3))
                    + " A"
                )
                print(
                    "Arms Current Diff: "
                    + str(round(self.read_bsmp_variable(37, "float"), 3))
                    + " A"
                )

                print(
                    "\nCapBank Voltage 1: "
                    + str(round(self.read_bsmp_variable(38, "float"), 3))
                    + " V"
                )
                print(
                    "CapBank Voltage 2: "
                    + str(round(self.read_bsmp_variable(39, "float"), 3))
                    + " V"
                )

                print(
                    "\nDuty-Cycle 1: "
                    + str(round(self.read_bsmp_variable(40, "float"), 3))
                    + " %"
                )
                print(
                    "Duty-Cycle 2: "
                    + str(round(self.read_bsmp_variable(41, "float"), 3))
                    + " %"
                )
                print(
                    "Differential Duty-Cycle: "
                    + str(round(self.read_bsmp_variable(42, "float"), 3))
                    + " %"
                )

                time.sleep(dt)

            self.set_slave_add(old_add)
        except:
            self.set_slave_add(old_add)
            raise

    def check_param_bank(self, param_file):
        fbp_param_list = []

        max_sampling_freq = 600000
        c28_sysclk = 150e6

        with open(param_file, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                fbp_param_list.append(row)

        for param in fbp_param_list:
            if str(param[0]) == "Num_PS_Modules" and param[1] > 4:
                print(
                    "Invalid " + str(param[0]) + ": " + str(param[1]) + ". Maximum is 4"
                )

            elif str(param[0]) == "Freq_ISR_Controller" and param[1] > 6000000:
                print(
                    "Invalid " + str(param[0]) + ": " + str(param[1]) + ". Maximum is 4"
                )

            else:
                for n in range(64):
                    try:
                        print(str(param[0]) + "[" + str(n) + "]: " + str(param[n + 1]))
                        print(self.set_param(str(param[0]), n, float(param[n + 1])))
                    except:
                        break

    def get_default_ramp_waveform(
        self, interval=500, nrpts=4000, ti=None, fi=None, forms=None
    ):
        from siriuspy.magnet.util import get_default_ramp_waveform

        return get_default_ramp_waveform(interval, nrpts, ti, fi, forms)

    def save_ramp_waveform(self, ramp):
        filename = input("Digite o nome do arquivo: ")
        with open(filename + ".csv", "w", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(ramp)

    def save_ramp_waveform_col(self, ramp):
        filename = input("Digite o nome do arquivo: ")
        with open(filename + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            for val in ramp:
                writer.writerow([val])

    def read_vars_fac_n(self, n=1, dt=0.5):
        old_add = self.get_slave_add()
        try:
            for i in range(n):
                print(
                    "\n--- Measurement #"
                    + str(i + 1)
                    + " ------------------------------------------\n"
                )
                self.set_slave_add(1)
                self.read_vars_fac_dcdc()
                print("\n-----------------------\n")
                self.set_slave_add(2)
                self.read_vars_fac_acdc()
                time.sleep(dt)
            self.set_slave_add(old_add)
        except:
            self.set_slave_add(old_add)

    def set_buf_samples_freq(self, fs):
        self.set_param("Freq_TimeSlicer", 1, fs)
        self.save_param_eeprom("Freq_TimeSlicer", 1)
        self.reset_udc()

    def calc_pi(self, r_load, l_load, f_bw, v_dclink, send_drs=0, dsp_id=0):
        kp = 2 * 3.1415 * f_bw * l_load / v_dclink
        ki = kp * r_load / l_load
        print("\n  Kp = " + str(kp))
        print("  Ki = " + str(ki) + "\n")
        if send_drs:
            self.set_dsp_coeffs(3, dsp_id, [kp, ki, 0.95, -0.95])
        return [kp, ki]

    def config_dsp_modules_drs_fap_tests(self):
        kp_load = 0
        ki_load = 20.95
        kp_share = 0.000032117
        ki_share = 0.0012

        drs.set_dsp_coeffs(3, 0, [kp_load, ki_load, 0.6, 0])
        drs.set_dsp_coeffs(3, 1, [kp_share, ki_share, 0.0015, -0.0015])
        drs.save_dsp_modules_eeprom()

    def set_prbs_sampling_freq(self, freq, type_memory):
        self.set_param("Freq_TimeSlicer", 0, freq)
        self.set_param("Freq_TimeSlicer", 1, freq)
        self.save_param_bank(type_memory)

    def get_dsp_modules_bank(
        self, list_dsp_classes=[1, 2, 3, 4, 5, 6], print_modules=1
    ):
        dsp_modules_bank = []
        for dsp_class in list_dsp_classes:
            for dsp_id in range(num_dsp_modules[dsp_class]):
                dsp_module = [dsp_classes_names[dsp_class], dsp_class, dsp_id]
                for dsp_coeff in range(num_coeffs_dsp_modules[dsp_class]):
                    try:
                        coeff = self.get_dsp_coeff(dsp_class, dsp_id, dsp_coeff)
                        if dsp_class == 3 and dsp_coeff == 1:
                            coeff *= self.get_param("Freq_ISR_Controller", 0)
                        dsp_module.append(coeff)
                    except:
                        dsp_module.append("nan")
                dsp_modules_bank.append(dsp_module)
                if print_modules:
                    print(dsp_module)

        return dsp_modules_bank

    def store_dsp_modules_bank_csv(self, bank):
        filename = input("Digite o nome do arquivo: ")
        with open(filename + ".csv", "w", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            for dsp_module in bank:
                writer.writerow(dsp_module)

    def set_dsp_modules_bank(self, dsp_modules_file, save_eeprom=0):
        dsp_modules_row = []
        with open(dsp_modules_file, newline="") as f:
            reader = csv.reader(f)

            for dsp_module in reader:
                if not dsp_module == []:
                    if not dsp_module[0][0] == "#":
                        list_coeffs = []

                        for coeff in dsp_module[
                            3 : 3 + num_coeffs_dsp_modules[int(dsp_module[1])]
                        ]:
                            list_coeffs.append(float(coeff))

                        print(
                            str(int(dsp_module[1]))
                            + " "
                            + str(int(dsp_module[2]))
                            + " "
                            + str(list_coeffs)
                        )
                        self.set_dsp_coeffs(
                            int(dsp_module[1]), int(dsp_module[2]), list_coeffs
                        )

        if save_eeprom:
            self.save_dsp_modules_eeprom()
        else:
            print(
                "\n *** Aviso: Os coeficientes configurados não foram salvos na memória EEPROM. Caso deseje salvar, utilize o argumento save_eeprom = 1"
            )

    def select_param_bank(self, cfg_dsp_modules=0):

        add = int(
            input(
                "\n Digite o endereco serial atual do controlador a ser configurado: "
            )
        )

        old_add = self.get_slave_add()
        self.set_slave_add(add)

        areas = ["IA", "LA", "PA"]
        ps_models = ["fbp", "fbp_dclink", "fap", "fap_4p", "fap_2p4s", "fac", "fac_2s"]
        ps_folders = [
            "fbp",
            "fbp_dclink",
            "fap",
            "fap",
        ]
        la_fap = [
            "TB-Fam:PS-B",
            "TS-01:PS-QF1A",
            "TS-01:PS-QF1B",
            "TS-02:PS-QD2",
            "TS-02:PS-QF2",
            "TS-03:PS-QF3",
            "TS-04:PS-QD4A",
            "TS-04:PS-QD4B",
            "TS-04:PS-QF4",
        ]

        print("\n Selecione area: \n")
        print("   0: Sala de racks")
        print("   1: Linhas de transporte")
        print("   2: Sala de fontes\n")
        area = int(input(" Digite o numero correspondente: "))

        if area == 0:
            sector = input("\n Digite o setor da sala de racks [1 a 20]: ")

            if int(sector) < 10:
                sector = "0" + sector

            rack = input("\n Escolha o rack em que a fonte se encontra [1/2/3]: ")

            # if (rack != '1') and (rack != '2'):
            if not ((rack == "1") or (rack == "2") or (sector == "09" and rack == "3")):
                print(" \n *** RACK INEXISTENTE ***\n")
                return

            print("\n Escolha o tipo de fonte: \n")
            print("   0: FBP")
            print("   1: FBP-DCLink\n")
            ps_model = int(input(" Digite o numero correspondente: "))

            if ps_model == 0:
                crate = "_crate_" + input(
                    "\n Digite a posicao do bastidor, de cima para baixo. Leve em conta os bastidores que ainda nao foram instalados : "
                )

            elif ps_model == 1:
                crate = ""

            else:
                print(" \n *** TIPO DE FONTE INEXISTENTE ***\n")
                return

            file_dir = "../ps_parameters/IA-" + sector + "/" + ps_models[ps_model] + "/"

            file_name = (
                "parameters_"
                + ps_models[ps_model]
                + "_IA-"
                + sector
                + "RaPS0"
                + rack
                + crate
                + ".csv"
            )

            file_path = file_dir + file_name

            print("\n Banco de parametros a ser utilizado: " + file_path)

        elif area == 1:

            print("\n Escolha o tipo de fonte: \n")
            print("   0: FBP")
            print("   1: FBP-DCLink")
            print("   2: FAP\n")

            ps_model = int(input(" Digite o numero correspondente: "))

            if ps_model == 0 or ps_model == 1:

                crate = input(
                    "\n Digite a posicao do bastidor, de cima para baixo. Leve em conta os bastidores que ainda nao foram instalados : "
                )
                ps_name = "_LA-RaPS06_crate_" + crate

                file_dir = "../ps_parameters/LA/" + ps_models[ps_model] + "/"
                file_name = "parameters_" + ps_models[ps_model] + ps_name + ".csv"
                file_path = file_dir + file_name

            elif ps_model == 2:

                ps_list = []

                file_dir = "../ps_parameters/LA/fap/"
                for entry in os.listdir(file_dir):
                    if os.path.isfile(os.path.join(file_dir, entry)):
                        ps_list.append(entry)

                print("\n ### Lista de fontes FAP da linha de transporte ### \n")

                for idx, ps in enumerate(ps_list):
                    print("   " + str(idx) + ": " + ps)

                ps_idx = int(input("\n Escolha o índice da fonte correspondente: "))

                file_path = file_dir + ps_list[ps_idx]

            else:
                print(" \n *** TIPO DE FONTE INEXISTENTE ***\n")
                return

            print("\n Banco de parametros a ser utilizado: " + file_path)

        elif area == 2:
            print("\n Escolha o tipo de fonte: \n")
            print("   0: FAC")
            print("   1: FAP\n")

            ps_model = int(input(" Digite o numero correspondente: "))

            if ps_model == 0:

                ps_list = []

                file_dir = "../ps_parameters/PA/fac/"
                for entry in os.listdir(file_dir):
                    if os.path.isfile(os.path.join(file_dir, entry)):
                        ps_list.append(entry)

                print(
                    "\n ### Lista de bastidores de controle FAC da sala de fontes ### \n"
                )

                for idx, ps in enumerate(ps_list):
                    print(" ", idx, ": ", ps)

                ps_idx = int(input("\n Escolha o índice da fonte correspondente: "))

                file_path = file_dir + ps_list[ps_idx]

            elif ps_model == 1:

                ps_list = []

                file_dir = "../ps_parameters/PA/fap/"
                for entry in os.listdir(file_dir):
                    if os.path.isfile(os.path.join(file_dir, entry)):
                        ps_list.append(entry)

                print(
                    "\n ### Lista de bastidores de controle FAP da sala de fontes ### \n"
                )

                for idx, ps in enumerate(ps_list):
                    print(" ", idx, ": ", ps)

                ps_idx = int(input("\n Escolha o índice da fonte correspondente: "))

                file_path = file_dir + ps_list[ps_idx]

            else:
                print(" \n *** TIPO DE FONTE INEXISTENTE ***\n")
                return

            print("\n Banco de parametros a ser utilizado: " + file_path)

        else:
            print(" \n *** SALA INEXISTENTE ***\n")
            return

        r = input("\n Tem certeza que deseja prosseguir? [Y/N]: ")

        if (r != "Y") and (r != "y"):
            print(" \n *** OPERAÇÃO CANCELADA ***\n")
            return
        self.set_slave_add(add)

        if ps_model == 0 and cfg_dsp_modules == 1:
            print("\n Enviando parametros de controle para controlador ...")

            dsp_file_dir = (
                "../dsp_parameters/IA-" + sector + "/" + ps_models[ps_model] + "/"
            )

            dsp_file_name = (
                "dsp_parameters_"
                + ps_models[ps_model]
                + "_IA-"
                + sector
                + "RaPS0"
                + rack
                + crate
                + ".csv"
            )

            dsp_file_path = dsp_file_dir + dsp_file_name

            self.set_dsp_modules_bank(dsp_file_path)

            print("\n Gravando parametros de controle na memoria ...")
            time.sleep(1)
            self.save_dsp_modules_eeprom()

        print("\n Enviando parametros de operacao para controlador ...\n")
        time.sleep(1)
        self.set_param_bank(file_path)
        print("\n Gravando parametros de operacao na memoria EEPROM onboard ...")
        self.save_param_bank(2)
        time.sleep(5)

        print("\n Resetando UDC ...")
        self.reset_udc()
        time.sleep(2)

        print(
            "\n Pronto! Não se esqueça de utilizar o novo endereço serial para se comunicar com esta fonte! :)\n"
        )

        self.set_slave_add(old_add)

    def get_siggen_vars(self):
        print("\n### SigGen Variables ###\n")
        print("Enable: " + str((round(self.read_bsmp_variable(6, "uint16_t"), 3))))
        print(
            "Type: "
            + list_sig_gen_types[int(round(self.read_bsmp_variable(7, "uint16_t"), 3))]
        )
        print("Num Cycles: " + str(round(self.read_bsmp_variable(8, "uint16_t"), 3)))
        print("Index: " + str(round(self.read_bsmp_variable(9, "float"), 3)))
        print("Frequency: " + str(round(self.read_bsmp_variable(10, "float"), 3)))
        print("Amplitude: " + str(round(self.read_bsmp_variable(11, "float"), 3)))
        print("Offset: " + str(round(self.read_bsmp_variable(12, "float"), 3)))

        self.read_var(self.index_to_hex(13))
        reply_msg = self.ser.read(21)
        val = struct.unpack("BBHffffB", reply_msg)

        print("Aux Param 0: " + str(val[3]))
        print("Aux Param 1: " + str(val[4]))
        print("Aux Param 2: " + str(val[5]))
        print("Aux Param 3: " + str(val[6]))

    def firmware_initialization(self):
        print("\n ### Inicialização de firmware ### \n")

        print("\n Lendo status...")
        print(self.read_ps_status())

        print("\n Lendo versão de firmware...")
        self.read_udc_version()

        print("\n Desbloqueando UDC...")
        print(self.unlock_udc(0xFFFF))

        print("\n Habilitando EEPROM onboard...")
        self.enable_onboard_eeprom()

        print("\n Alterando senha...")
        print(self.set_param("Password", 0, 0xCAFE))
        print(self.save_param_eeprom("Password", 0, 2))

        print("\n Configurando banco de parâmetros...")
        self.select_param_bank()

        print("\n ### Fim da inicialização de firmware ### \n")

    def cfg_hensys_ps_model(self):

        list_files = [
            "fbp_dclink/parameters_fbp_dclink_hensys.csv",
            "fac/parameters_fac_acdc_hensys.csv",
            "fac/parameters_fac_dcdc_hensys.csv",
            "fac/parameters_fac_2s_acdc_hensys.csv",
            "fac/parameters_fac_2s_dcdc_hensys.csv",
            "fac/parameters_fac_2p4s_acdc_hensys.csv",
            "fac/parameters_fac_2p4s_dcdc_hensys.csv",
            "fap/parameters_fap_hensys.csv",
            "fap/parameters_fap_2p2s_hensys.csv",
            "fap/parameters_fap_4p_hensys.csv",
        ]

        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(0xCAFE))

        print("\n *** Escolha o modelo de fonte a ser configurado ***\n")
        print(" 0: FBP-DClink")
        print(" 1: FAC-ACDC")
        print(" 2: FAC-DCDC")
        print(" 3: FAC-2S-ACDC")
        print(" 4: FAC-2S-DCDC")
        print(" 5: FAC-2P4S-ACDC")
        print(" 6: FAC-2P4S-DCDC")
        print(" 7: FAP")
        print(" 8: FAP-2P2S")
        print(" 9: FAP-4P")

        model_idx = int(input("\n Digite o índice correspondente: "))
        file_path = "../ps_parameters/development/" + list_files[model_idx]

        print("\n Banco de parametros a ser utilizado: " + file_path)

        r = input("\n Tem certeza que deseja prosseguir? [Y/N]: ")

        if (r != "Y") and (r != "y"):
            print(" \n *** OPERAÇÃO CANCELADA ***\n")
            return

        print("\n Enviando parametros de operacao para controlador ...\n")
        time.sleep(1)
        self.set_param_bank(file_path)

        print("\n Gravando parametros de operacao na memoria EEPROM onboard ...")
        self.save_param_bank(2)
        time.sleep(5)

        print("\n Resetando UDC ...")
        self.reset_udc()
        time.sleep(2)

        print(
            "\n Pronto! Nao se esqueca de utilizar o novo endereco serial para se comunicar com esta fonte! :)\n"
        )

    def test_bid_board(self, password):

        r = input(
            "\n Antes de iniciar, certifique-se que o bastidor foi energizado sem a placa BID.\n Para prosseguir, conecte a placa BID a ser testada e pressione qualquer tecla... "
        )

        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))

        print("\n Carregando banco de parametros da memoria onboard ...")
        print(self.load_param_bank(type_memory=2))

        print("\n Banco de parametros da memoria onboard:\n")

        max_param = list_parameters.index("Scope_Source")
        param_bank_onboard = []

        for param in list_parameters[0:max_param]:
            val = self.get_param(param, 0)
            print(param + ":", val)
            param_bank_onboard.append(val)

        print("\n Salvando banco de parametros na memoria offboard ...")
        print(self.save_param_bank(type_memory=1))

        time.sleep(5)

        print("\n Resetando UDC ...")
        self.reset_udc()

        time.sleep(3)

        self.read_ps_status()

        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))

        print("\n Carregando banco de parametros da memoria offboard ...")
        print(self.load_param_bank(type_memory=1))

        self.read_ps_status()

        print("\n Verificando banco de parametros offboard apos reset ... \n")
        try:
            param_bank_offboard = []

            for param in list_parameters[0:max_param]:
                val = self.get_param(param, 0)
                print(param, val)
                param_bank_offboard.append(val)

            if param_bank_onboard == param_bank_offboard:
                print("\n Placa BID aprovada!\n")
            else:
                print("\n Placa BID reprovada!\n")

        except:
            print(" Placa BID reprovada!\n")

    def upload_parameters_bid(self, password):
        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))

        print("\n Carregando banco de parametros da memoria offboard ...")
        print(self.load_param_bank(type_memory=1))
        time.sleep(1)

        print("\n Salvando banco de parametros na memoria onboard ...")
        print(self.save_param_bank(type_memory=2))
        time.sleep(5)

        print("\n Carregando coeficientes de controle da memoria offboard ...")
        print(self.load_dsp_modules_eeprom(type_memory=1))
        time.sleep(1)

        print("\n Salvando coeficientes de controle na memoria onboard ...\n")
        print(self.save_dsp_modules_eeprom(type_memory=2))

    def download_parameters_bid(self, password):
        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))

        print("\n Carregando banco de parametros da memoria onboard ...")
        print(self.load_param_bank(type_memory=2))
        time.sleep(1)

        print("\n Salvando banco de parametros na memoria offboard ...")
        print(self.save_param_bank(type_memory=1))
        time.sleep(5)

        print("\n Carregando coeficientes de controle da memoria onboard ...")
        print(self.load_dsp_modules_eeprom(type_memory=2))
        time.sleep(1)

        print("\n Salvando coeficientes de controle na memoria offboard ...")
        print(self.save_dsp_modules_eeprom(type_memory=1))
