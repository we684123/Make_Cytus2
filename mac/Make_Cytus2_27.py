#/usr/bin/python
#coding=utf-8

import os
import re
import sys
import json
import copy
from io import open
from os import listdir
from pprint import pprint
from os.path import isfile, join

#check python version
pyver = sys.version_info[0]

def creat_flie(fliename, text):
	try:
		f = open(fliename, 'w+', encoding='utf8')
		if pyver is 2:
			i = f.write(unicode(text))
		else:
			i = f.write(text)
		f.close()
		return 0
	except Exception as e:
		raise
		return e

def creat_C2(V2_data):
	C2_data = {
		"format_version": V2_data["format_version"],
		"time_base": V2_data["time_base"],
		"start_offset_time": 0,
		"page_list": [],
		"tempo_list": [{"tick": 0, "value": 0}],
		"event_order_list": V2_data["event_order_list"],
		"note_list": []
	}
	C2_data["tempo_list"][0]["value"] = V2_data["value"]

	# 創造不會多給資料
	C2_data["note_list"] = creat_note_list(V2_data)
	C2_data["page_list"] = creat_page_list(V2_data)
	return C2_data

#y = creat_note_list(V2_data)


def creat_note_list(V2_data):
	note_list = []
	note_template = {
		"page_index": 0,
		"type": 0,
		"id": 0,
		"tick": 0,
		"x": 0.100000001490116,
		"has_sibling": False,
		"hold_tick": 0,
		"next_id": 0,
		"is_forward": False
	}
	for i in range(0, len(V2_data["note_list"])):
		# print(i)
		note_template["page_index"] = V2_data["note_list"][i]["C2_page_index"]
		note_template["type"] = V2_data["note_list"][i]["C2_type"]
		note_template["id"] = V2_data["note_list"][i]["id"]
		note_template["tick"] = V2_data["note_list"][i]["C2_tick"]
		note_template["x"] = V2_data["note_list"][i]["x"]
		note_template["hold_tick"] = V2_data["note_list"][i]["C2_hold_tick"]
		if V2_data["note_list"][i]["next_id"] == -1:
			note_template["next_id"] = 0
		else:
			note_template["next_id"] = V2_data["note_list"][i]["next_id"]
		if V2_data["note_list"][i]["end_id"] == 1:
			note_template["next_id"] = -1
		note_list.append(copy.copy(note_template))
		# print(json.dumps(note_list))
	return note_list


def creat_page_list(V2_data):
	page_list = copy.copy(V2_data["page_list"])
	for v in page_list:
		del v["page_id"]
	page_list[0]["scan_line_direction"] = page_list[2]["scan_line_direction"]
	return page_list


def reset_page_list(V2_data):
	len_note_list = len(V2_data["note_list"])
	total_chart = V2_data["note_list"][len_note_list - 1]["C2_page_index"]
	end_page_up_down = V2_data["note_list"][len_note_list - 1]["up_down"]
	page_list = []
	for i in range(total_chart - 1, -1, -1):
		end_tick = (i + 1) * 960
		start_tick = end_tick - 960
		if i % 2:
			if end_page_up_down == 222:
				scan_line_direction = -1
			else:
				scan_line_direction = 1
		else:
			if end_page_up_down == 222:
				scan_line_direction = 1
			else:
				scan_line_direction = -1
		# print(i)
		page_list_template = {
			"start_tick": start_tick,
			"end_tick": end_tick,
			"scan_line_direction": scan_line_direction
		}
		page_list.append(page_list_template)
	page_list.reverse()
	return page_list


def V2_to_C2(V2_data):
	# V2_data = offset_PAGE_SHIFT(V2_data)  # 抵消掉PAGE_SHIFT帶來的誤差
	# 抵消掉抵銷的時間...，到底喔...
	#V2_data = offset_offset_PAGE_SHIFT(V2_data)
	#V2_data = offset_offset_PAGE_SHIFT(V2_data)
	if float(V2_data["extension_of_time"]) != 0:
		V2_data = extension_of_time(V2_data)  # 同時加減時間
	V2_data = Bind(V2_data)  # 綁定link(下一個)
	V2_data = supplement_next_id(V2_data)  # 綁定link(最後補-1)
	V2_data = supplement_C2noteType(V2_data)  # 綁定C2的note_type
	V2_data = supplement_C2tempo_list_value(V2_data)  # 設定C2的value
	V2_data = supplement_C2_tick(V2_data)  # 轉換C2_note的時間成tick
	V2_data = supplement_C2_hold_tick(V2_data)  # 轉換C2_note_hold的時間成tick
	V2_data = supplement_end_id(V2_data)  # 將是否為link結尾標記出來 是=1 否=0

	# 綁定C2的page_index #這個看要之後重綁還是直接移到後面並重做
	V2_data = supplement_C2page_index(V2_data)
	V2_data = supplement_C2_up_down(V2_data)  # 綁定掃線上下 #這個看要之後重綁還是直接移到後面並重做
	# 綁定C2的page_id #這個看要之後重綁還是直接移到後面並重做
	V2_data = supplement_C2page_id(V2_data)
	# 綁定C2的page_id  #這個看要之後重綁還是直接移到後面並重做
	V2_data = supplement_C2_page_list_id(V2_data)

	# V2_data = click_error(V2_data) #進行錯誤偵測，並補上資料
	# V2_data = fix_hold_error(V2_data)
	return V2_data


def extension_of_time(V2_data):
	extension = float(V2_data["extension_of_time"])
	# note_list
	for i in range(0, len(V2_data["note_list"])):
		note_time = float(V2_data["note_list"][i]["time"])
		t = extension + note_time
		V2_data["note_list"][i]["time"] = t
	# BPM_list
	for i in range(0, len(V2_data["BPM_list"])):
		bpm_time = float(V2_data["BPM_list"][i]["time"])
		t = extension + bpm_time
		V2_data["BPM_list"][i]["time"] = t
	# CHC_list
	for i in range(0, len(V2_data["CHC_list"])):
		chc_time = float(V2_data["CHC_list"][i]["time"])
		t = extension + chc_time
		V2_data["CHC_list"][i]["time"] = t
	return V2_data


def offset_offset_PAGE_SHIFT(V2_data):
	PAGE_SHIFT = float(V2_data["PAGE_SHIFT"])
	C1_PAGE_SIZE = float(V2_data["PAGE_SIZE"])
	setoff_time = (PAGE_SHIFT % C1_PAGE_SIZE)
	#setoff_time = 0
	for i in range(0, len(V2_data["note_list"])):
		note_time = float(V2_data["note_list"][i]["time"])
		V2_data["note_list"][i]["time"] = note_time - setoff_time
	return V2_data


def fix_hold_error(V2_data):
	for i in range(0, len(V2_data["note_list"])):
		# tick_out 偵測
		C2_hold_tick = V2_data["note_list"][i]["C2_hold_tick"]
		hold_tick_out = V2_data["note_list"][i]["hold_tick_out"]

		if C2_hold_tick > 0 and hold_tick_out == 99999:
			C2_page_index = V2_data["note_list"][i]["C2_page_index"]
			V2_data["note_list"][i]["C2_page_index"] = C2_page_index + 1
			page_list_id = V2_data["note_list"][i]["page_list_id"]
			V2_data["note_list"][i]["page_list_id"] = page_list_id + 1
			start_tick = V2_data["note_list"][i]["start_tick"]
			V2_data["note_list"][i]["start_tick"] = start_tick + 960
			end_tick = V2_data["note_list"][i]["end_tick"]
			V2_data["note_list"][i]["end_tick"] = end_tick + 960
			up_down = V2_data["note_list"][i]["up_down"]
			if up_down == 222:
				V2_data["note_list"][i]["up_down"] = 8888
			else:
				V2_data["note_list"][i]["up_down"] = 222
			V2_data["note_list"][i]["fix_error"] = 1

		elif C2_hold_tick > 0 and hold_tick_out == 88888:
			V2_data["note_list"][i]["C2_type"] = 2
			V2_data["note_list"][i]["fix_error"] = 1

		else:
			V2_data["note_list"][i]["fix_error"] = 0
	return V2_data


def click_error(V2_data):
	for i in range(0, len(V2_data["note_list"])):
		# tick_out 偵測標記
		C2_tick = V2_data["note_list"][i]["C2_tick"]
		start_tick = V2_data["note_list"][i]["start_tick"]
		end_tick = V2_data["note_list"][i]["end_tick"]
		tick_page = V2_data["note_list"][i]['tick_page']
		if (C2_tick > end_tick) or (C2_tick < start_tick):
			V2_data["note_list"][i]["note_tick_out"] = 99999
		else:
			V2_data["note_list"][i]["note_tick_out"] = 0

		#i = 308
		# hold_tick 過界偵測
		hold_tick = float(V2_data["note_list"][i]["C2_hold_tick"])
		all_tick = C2_tick + hold_tick
		if (all_tick > end_tick) or (all_tick < start_tick):
			if hold_tick > tick_page:
				V2_data["note_list"][i]["hold_tick_out"] = 88888
			else:
				V2_data["note_list"][i]["hold_tick_out"] = 99999
		else:
			V2_data["note_list"][i]["hold_tick_out"] = 0
		V2_data["note_list"][i]["fix_error"] = 0
	return V2_data


def supplement_C2_page_list_id(V2_data):
	for i in range(0, len(V2_data["note_list"])):
		page_list_id = V2_data["note_list"][i]["C2_page_index"]
		V2_data["note_list"][i]["page_list_id"] = page_list_id - 1
	return V2_data


def supplement_C2page_id(V2_data):
	for i in range(0, len(V2_data["note_list"])):
		note_time = float(V2_data["note_list"][i]["time"])
		end_tick = (V2_data["note_list"][i]["C2_page_index"]) * 960
		start_tick = end_tick - 960
		V2_data["note_list"][i]["start_tick"] = start_tick
		V2_data["note_list"][i]["end_tick"] = end_tick
	return V2_data


def offset_PAGE_SHIFT(V2_data):
	PAGE_SHIFT = float(V2_data["PAGE_SHIFT"])
	C1_PAGE_SIZE = float(V2_data["PAGE_SIZE"])
	setoff_time = (PAGE_SHIFT % C1_PAGE_SIZE)
	#setoff_time = 0
	for i in range(0, len(V2_data["note_list"])):
		note_time = float(V2_data["note_list"][i]["time"])
		V2_data["note_list"][i]["time"] = note_time + setoff_time
	return V2_data


def output_V1plus(fliename, V2_data_Bind_sup):  # 雖然不是純 V1 www
	text = 'BPM\t' + str(int(V2_data_Bind_sup["BPM"])) + '\n'
	text = text + 'PAGE_SHIFT\t' + str(V2_data_Bind_sup["PAGE_SHIFT"]) + '\n'
	text = text + 'PAGE_SIZE\t' + str(V2_data_Bind_sup["PAGE_SIZE"]) + '\n'
	text = text + 'value\t' + str(V2_data_Bind_sup["value"]) + '\n'

	col_name = [
		"c1v2NoteType",
		"tc1v2NoteId",
		"tc1v2NoteTime",
		"tc1v2NoteX",
		"tc1v2HoldTime",
		"tc1v1NextLink",
		"c2v0NoteType",
		"c2v0PageListId(first is 1)",
		"c2v0PageListId(first is 0)",
		"c2v0NoteTick",
		"c2v0HoldTick",
		"c2v0scan_line_direction(8888_up,222_down)",
		"c2v0IsLinkEnd?(1=y,0=n)",
		"c2v0StartTick",
		"c2v0EndTick",
		"NoteTimeOverrun",
		"HoldTimeOverrun",
		"FixHoldError"
	]
	for j in range(0, len(col_name)):
		text += str(col_name[j]) + '\t'
	text += '\n'

	V2_data_Bind_len = len(V2_data_Bind_sup["note_list"])
	n = V2_data_Bind_sup["note_list"]
	for i in range(0, V2_data_Bind_len):
		note = [
			str(n[i]["type"]),
			str(n[i]["id"]),
			str(n[i]["time"]),
			str(n[i]["x"]),
			str(n[i]["hold"]),
			str(n[i]["next_id"]),
			str(n[i]["C2_type"]),
			str(n[i]["C2_page_index"]),
			str(n[i]["page_list_id"]),
			str(n[i]["C2_tick"]),
			str(n[i]["C2_hold_tick"]),
			str(n[i]["up_down"]),
			str(n[i]["end_id"]),
			str(n[i]["start_tick"]),
			str(n[i]["end_tick"]),
			str(n[i]["note_tick_out"]),
			str(n[i]["hold_tick_out"]),
			str(n[i]["fix_error"])
		]
		for k in range(0, len(note)):
			text += str(note[k]) + '\t'
		text += '\n'
	try:
		f = open(fliename + ".v1plus", 'w+', encoding='utf8')
		if pyver is 2:
			i = f.write(unicode(text))
		else:
			i = f.write(text)
		return 0
	except Exception as e:
		raise
		return e


def creat_C2V0plus(V2_data):
	C2_data = {
		"format_version": V2_data["format_version"],
		"time_base": V2_data["time_base"],
		"start_offset_time": 0,
		"page_list": [],
		"tempo_list": [{"tick": 0, "value": 0}],
		"event_order_list": V2_data["event_order_list"],
		"note_list": []
	}
	C2_data["tempo_list"][0]["value"] = V2_data["value"]

	# 創造不會多給資料
	C2_data["note_list"] = V2_data["note_list"]
	C2_data["page_list"] = V2_data["page_list"]

	return C2_data


def supplement_C2_up_down(V2_data):
	PAGE_SHIFT = float(V2_data["PAGE_SHIFT"])
	C1_PAGE_SIZE = float(V2_data["PAGE_SIZE"])
	for i in range(0, len(V2_data["note_list"])):
		note_time = float(V2_data["note_list"][i]["time"])
		if PAGE_SHIFT >= 1:
			if int((note_time + PAGE_SHIFT % 1 / C1_PAGE_SIZE) / C1_PAGE_SIZE) % 2:
				V2_data["note_list"][i]["up_down"] = 8888  # 8888
			else:
				V2_data["note_list"][i]["up_down"] = 222  # 222
		else:
			if int((note_time + PAGE_SHIFT % 1 / C1_PAGE_SIZE) / C1_PAGE_SIZE) % 2:
				V2_data["note_list"][i]["up_down"] = 222  # 222
			else:
				V2_data["note_list"][i]["up_down"] = 8888  # 8888
	return V2_data


def supplement_C2_hold_tick(V2_data):
	value = V2_data["value"]
	BPM = float(V2_data["conversion_constant"]) / value
	Beats = int(V2_data["beat"])
	C1_PAGE_SIZE = 60 * Beats / BPM / 2
	start_to_end_tick_base = 960
	s_tick = C1_PAGE_SIZE / start_to_end_tick_base
	for i in range(0, len(V2_data["note_list"])):
		if float(V2_data["note_list"][i]["hold"]) == 0:
			V2_data["note_list"][i]["C2_hold_tick"] = 0
			continue
		note_hold_time = float(V2_data["note_list"][i]["hold"])
		C2_hold_tick = int(note_hold_time / s_tick)
		V2_data["note_list"][i]["C2_hold_tick"] = C2_hold_tick
	return V2_data


def supplement_C2_tick(V2_data):
	value = V2_data["value"]
	BPM = float(V2_data["conversion_constant"]) / value
	Beats = int(V2_data["beat"])
	C1_PAGE_SIZE = 60 * Beats / BPM / 2
	start_to_end_tick_base = 960
	s_tick = C1_PAGE_SIZE / start_to_end_tick_base
	#PAGE_SHIFT = float(V2_data["PAGE_SHIFT"])
	for i in range(0, len(V2_data["note_list"])):
		note_time = float(V2_data["note_list"][i]["time"])
		C2_tick = int(note_time / s_tick)
		V2_data["note_list"][i]["C2_tick"] = C2_tick
	return V2_data


def supplement_C2tempo_list_value(V2_data):
	BPM = float(V2_data["BPM"])
	value = float(V2_data["conversion_constant"]) / BPM
	V2_data["value"] = int(value) * 2
	return V2_data


def supplement_C2page_index(V2_data_type_sup):
	BPM = float(V2_data_type_sup["BPM"])
	PAGE_SHIFT = float(V2_data_type_sup["PAGE_SHIFT"])
	PAGE_SIZE = float(V2_data_type_sup["PAGE_SIZE"])
	for i in range(0, len(V2_data_type_sup["note_list"])):
		note_time = float(V2_data_type_sup["note_list"][i]["time"])
		page_index = int((note_time - (PAGE_SHIFT % PAGE_SIZE) +
						  PAGE_SHIFT % 1 / PAGE_SIZE) / PAGE_SIZE)
		V2_data_type_sup["note_list"][i]["C2_page_index"] = page_index
	return V2_data_type_sup


def supplement_C2noteType_ToAllNote(V2_data_Bind_sup):
	for i in range(0, len(V2_data_Bind_sup["note_list"])):
		V2_data_Bind_sup["note_list"][i]["C2_type"] = 0
	return V2_data_Bind_sup


def supplement_C2noteType_ToLinkBody(V2_data_Bind_sup):
	for i in range(0, len(V2_data_Bind_sup["link_list"])):
		link_len = len(V2_data["link_list"][i]["id_list"])
		for j in range(0, link_len):
			id = int(V2_data_Bind_sup["link_list"][i]["id_list"][j])
			V2_data_Bind_sup["note_list"][id]["C2_type"] = 4
	return V2_data_Bind_sup


def supplement_C2noteType_ToLinkhead(V2_data_Bind_sup):
	for i in range(0, len(V2_data_Bind_sup["link_list"])):
		id = int(V2_data_Bind_sup["link_list"][i]["id_list"][0])
		V2_data_Bind_sup["note_list"][id]["C2_type"] = 3
	return V2_data_Bind_sup


def supplement_C2noteType_ToHold(V2_data_Bind_sup):
	for i in range(0, len(V2_data_Bind_sup["note_list"])):
		if float(V2_data_Bind_sup["note_list"][i]["hold"]) > 0:
			V2_data_Bind_sup["note_list"][i]["C2_type"] = 1
	return V2_data_Bind_sup


def supplement_C2noteType_ToHold2(V2_data_Bind_sup):
	for i in range(0, len(V2_data_Bind_sup["note_list"])):
		if str(V2_data_Bind_sup["note_list"][i]["type"]) == "HOLD":
			V2_data_Bind_sup["note_list"][i]["C2_type"] = 1
	return V2_data_Bind_sup


def supplement_C2noteType_ToLONG(V2_data_Bind_sup):
	for i in range(0, len(V2_data_Bind_sup["note_list"])):
		if str(V2_data_Bind_sup["note_list"][i]["type"]) == "LONG":
			V2_data_Bind_sup["note_list"][i]["C2_type"] = 2
	return V2_data_Bind_sup


def supplement_C2noteType_ToSLIDE(V2_data_Bind_sup):
	for i in range(0, len(V2_data_Bind_sup["note_list"])):
		if str(V2_data_Bind_sup["note_list"][i]["type"]) == "SLIDE":
			V2_data_Bind_sup["note_list"][i]["C2_type"] = 5
	return V2_data_Bind_sup


def supplement_C2noteType(V2_data_Bind_sup):
	V2_data_Bind_sup = supplement_C2noteType_ToAllNote(V2_data_Bind_sup)
	V2_data_Bind_sup = supplement_C2noteType_ToHold(V2_data_Bind_sup)
	V2_data_Bind_sup = supplement_C2noteType_ToHold2(V2_data_Bind_sup)
	V2_data_Bind_sup = supplement_C2noteType_ToLONG(V2_data_Bind_sup)
	V2_data_Bind_sup = supplement_C2noteType_ToSLIDE(V2_data_Bind_sup)

	V2_data_Bind_sup = supplement_C2noteType_ToLinkBody(V2_data_Bind_sup)
	V2_data_Bind_sup = supplement_C2noteType_ToLinkhead(V2_data_Bind_sup)
	return V2_data_Bind_sup


def supplement_end_id(V2_data):
	for i in range(0, len(V2_data["note_list"])):
		V2_data["note_list"][i]["end_id"] = 0
	for j in range(0, len(V2_data["link_list"])):
		link_len = len(V2_data["link_list"][j]["id_list"])
		id = int(V2_data["link_list"][j]["id_list"][link_len - 1])
		V2_data["note_list"][id]["end_id"] = 1
	return V2_data


def supplement_next_id(V2_data_Bind):
	for i in range(0, len(V2_data_Bind["note_list"])):
		try:
			V2_data_Bind["note_list"][i]["next_id"]
		except Exception as e:
			V2_data_Bind["note_list"][i]["next_id"] = -1
	return V2_data_Bind


def Bind(V2_data):
	len(V2_data["link_list"])
	for i in range(0, len(V2_data["link_list"])):
		link_len = len(V2_data["link_list"][i]["id_list"])
		if link_len > 1:
			for j in range(0, link_len - 1):
				id = int(V2_data["link_list"][i]["id_list"][j])
				V2_data["note_list"][id]["next_id"] = V2_data["link_list"][i]["id_list"][j + 1]
	return V2_data


def get_extension(filename, reciprocal):
	extension = filename.split(".")[reciprocal]
	return extension


def get_V2_text(fliename):
	try:
		f = open(fliename, 'r+', encoding='utf8')
		t = f.read()
		f.close()
		return t
	except Exception as e:
		raise
		return e


def get_V2_data(V2_text):
	n = V2_text.split("\n")
	ctrl_line = 11
	data = {
		"VERSION": int(n[0].split(" ")[-1]),
		"BPM": float(n[1].split(" ")[-1]),
		"PAGE_SHIFT": float(n[2].split(" ")[-1]),
		"PAGE_SIZE": float(n[3].split(" ")[-1]),
		"scan_line_direction_opposite": int(n[4].split(" ")[-1]),
		"extension_of_time": float(n[5].split(" ")[-1]),
		"auto_fix_type": int(n[6].split(" ")[-1]),
		"format_version": int(n[7].split(" ")[-1]),
		"beat": int(n[8].split(" ")[-1]),
		"time_base": int(n[9].split(" ")[-1]),
		"conversion_constant": int(n[10].split(" ")[-1]),
		"note_list": [],
		"link_list": [],
		"CHC_list": [],
		"BPM_list": []
	}
	for i in range(ctrl_line, len(n)):
		rt = get_type(n[i])
		# print(i)
		# print(rt)
		# print("-------")
		if rt == 'NOTE':
			j = n[i].split('\t')
			k = {
				"type": "NOTE",
				"id": int(j[1]),
				"time": float(j[2]),
				"x": float(j[3]),
				"hold": float(j[4])
			}
			data["note_list"].append(k)
		elif rt == 'LINK':
			j = n[i].split(' ')
			k = {
				"type": "LINK",
				"id_list": []
			}
			del j[0]
			k["id_list"] = j
			data["link_list"].append(k)
		elif rt == 'CHC':
			j = n[i].split('\t')
			k = {
				"type": "CHC",
				"mode": int(j[1]),
				"time": float(j[2]),
			}
			data["CHC_list"].append(k)
		elif rt == 'BPM':
			j = n[i].split('\t')
			k = {
				"type": "BPM",
				"BPM": float(j[1]),
				"time": float(j[2]),
			}
			data["BPM_list"].append(k)
		elif rt == 'SLIDE':
			j = n[i].split('\t')
			k = {
				"type": "SLIDE",
				"id": int(j[1]),
				"time": float(j[2]),
				"x": float(j[3]),
				"hold": float(j[4])
			}
			data["note_list"].append(k)
		elif rt == 'LONG':
			j = n[i].split('\t')
			k = {
				"type": "LONG",
				"id": int(j[1]),
				"time": float(j[2]),
				"x": float(j[3]),
				"hold": float(j[4])
			}
			data["note_list"].append(k)
		elif rt == 'HOLD':
			j = n[i].split('\t')
			k = {
				"type": "HOLD",
				"id": int(j[1]),
				"time": float(j[2]),
				"x": float(j[3]),
				"hold": float(j[4])
			}
			data["note_list"].append(k)
	return data
# -------------------------------------------------------------------------------


def get_type(t):
	# print(t)
	# print(type(t))
	s = ""
	i = 0
	while 1:
		# print("-------")
		# print(i)
		# print(t[i])

		if t[i] == " " or t[i] == "\t":
			# print(s)
			return s
		else:
			s += t[i]
		i += 1


def chang_CHC_BPM(V2_data):
	page_list = get_new_page_list(V2_data)
	V2_data = reset_page_index(V2_data, page_list)
	page_list = reset_page_list_up_down(V2_data, page_list)
	event_order_list = set_CHC(V2_data)
	V2_data["page_list"] = page_list
	V2_data["event_order_list"] = event_order_list
	return V2_data


def get_new_page_list(V2_data):
	end_tick = 0
	o_page_time = float(V2_data["PAGE_SIZE"])
	page_base = 960
	len_note_list = len(V2_data["note_list"])
	O_bpm = float(V2_data["BPM"])
	# set_bpm = set_bpm.clear()
	set_bpm = V2_data["BPM_list"].copy()
	set_bpm.insert(0, {'BPM': O_bpm, 'time': 0, 'type': 'BPM'})  # 插入原始BPM較好處理
	end_time = float(V2_data["note_list"][len_note_list - 1]["time"])
	set_bpm.append({'BPM': set_bpm[len(set_bpm) - 1]['BPM'],
					'time': end_time, 'type': 'BPM'})  # 插入最後的BPM較好處理
	page_list = []
	page_id = 0
	# l=1
	for l in range(0, len(set_bpm)): # 按變BPM的批次處理page_list
		now_bpm = set_bpm[l]["BPM"]
		proportion_to_tick = O_bpm / now_bpm #生成endtick的比例
		#proportion_to_list = now_bpm / O_bpm #生成所需list的比例
		if l >= (len(set_bpm) - 1): # 沒了 跳離
			break
			# set_bpm[3]
		# print("l = ",l)
		near = float(set_bpm[l + 1]["time"]) / (o_page_time * proportion_to_tick)
		# near 是一開始到第一個"變BPM"要生的幕數，
		if round(near % 1, 1):
			w = 1
		else:
			w = 0
		v = int(near) + w # 有多的要加1幕

		for k in range(v): # 開始生"幕"
			# print("k = ",k)
			start_tick = end_tick
			end_tick = end_tick + (page_base * proportion_to_tick)
			i = end_tick
			page_list_template = {
				"start_tick": int(start_tick),
				"end_tick": int(end_tick),
				"scan_line_direction": -1,
				"page_id": int(page_id)
			}
			page_list.append(page_list_template)
			page_id += 1
		# page_list
	return page_list


def time_to_C2tick(V2_data, time):
	value = V2_data["value"]
	BPM = float(V2_data["conversion_constant"]) / value
	Beats = int(V2_data["beat"])
	C1_PAGE_SIZE = 60 * Beats / BPM / 2
	start_to_end_tick_base = 960
	s_tick = C1_PAGE_SIZE / start_to_end_tick_base
	#PAGE_SHIFT = float(V2_data["PAGE_SHIFT"])
	note_time = float(time)
	C2_tick = int(note_time / s_tick)
	return C2_tick
# time_to_C2tick(V2_data, 91.935768)


def offset_PAGE_SHIFT_of_time(V2_data, time):
	PAGE_SHIFT = float(V2_data["PAGE_SHIFT"])
	C1_PAGE_SIZE = float(V2_data["PAGE_SIZE"])
	setoff_time = (PAGE_SHIFT % C1_PAGE_SIZE)
	re_time = float(time) + float(setoff_time)
	return re_time


def reset_page_index(V2_data, page_list):
	page_list_pointer = 0
	i = 0
	while i < len(V2_data["note_list"]):
		cut = V2_data["note_list"]
		x = cut[i]["C2_tick"]
		# print(page_list_pointer)
		#print("i =", i)

		st = page_list[page_list_pointer]["start_tick"]
		ed = page_list[page_list_pointer]["end_tick"]
		#print("st =", st)
		#print("x =", x)
		#print("ed =", ed)
		#print(x < ed and x > st)
		# print("-----------------------")
		if x <= ed and x > st:
			cut[i]['C2_page_index'] = page_list_pointer
			cut[i]['start_tick'] = st
			cut[i]['end_tick'] = ed
			cut[i]['tick_page'] = ed - st
			i += 1
		else:
			page_list_pointer += 1
	return reset_page_up_down(V2_data)
# i=0
# page_list[143]["start_tick"]
# page_list[106]["start_tick"]


def reset_page_up_down(V2_data):
	# opposite = 0
	# opposite = 1
	opposite = V2_data["scan_line_direction_opposite"]
	for i in range(0, len(V2_data["note_list"])):
		cut = V2_data["note_list"]
		yy = cut[i]["C2_page_index"] % 2
		#print("i =",i)
		#print("yy = ",yy)
		if opposite == 0:
			if yy == 1:
				cut[i]["up_down"] = 8888
			else:
				cut[i]["up_down"] = 222
		else:
			if yy == 1:
				cut[i]["up_down"] = 222
			else:
				cut[i]["up_down"] = 8888
		# print(cut[i]["up_down"])
	return V2_data


def reset_page_list_up_down(V2_data, page_list):
	# 將上面8888 222 結果同步回去page_list
	len_note_list = len(V2_data["note_list"])
	end_page_up_down = V2_data["note_list"][len_note_list - 1]["up_down"]
	len_page_list = len(page_list)
	for k in range(len_page_list - 1, 0, -1):
		# print(k)
		if k % 2:
			if end_page_up_down == 222:
				page_list[k]["scan_line_direction"] = -1
			else:
				page_list[k]["scan_line_direction"] = 1
		else:
			if end_page_up_down == 222:
				page_list[k]["scan_line_direction"] = 1
			else:
				page_list[k]["scan_line_direction"] = -1
	return page_list
# i=20


def set_CHC(V2_data):
	event_order_list = []
	CHC_list = V2_data["CHC_list"]
	for i in range(0, len(CHC_list)):
		yyyy = offset_PAGE_SHIFT_of_time(V2_data, CHC_list[i]["time"])
		tick = time_to_C2tick(V2_data, yyyy)
		if CHC_list[i]["mode"] == 1:
			type = 0
			args = 'R'
		else:
			type = 1
			args = 'G'

		CHC_template = {
			"tick": tick,
			"event_list": [{
				"type": type,  # 1+G 0+R
				"args": args
			}]
		}
		event_order_list.append(CHC_template)
	return event_order_list


# ======================================================================
mypath = os.getcwd()
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# i=1
for i in range(0, len(onlyfiles)):
	j = str(onlyfiles[i])
	fliename = j
	if get_extension(j, -1) == 'txt' and (get_extension(j, -2) == 'hard' or get_extension(j, -2) == 'esey'):
		V2_fliename = fliename
		V2_data = get_V2_data(get_V2_text(j))
		# pprint(V2_data)
		# V2_data.clear()
		V2_data = V2_to_C2(V2_data)
		# 至此V2_data為正常V2轉C2V0的所有所需，且click_error、fix_hold_error的部分暫緩
		# 現在將在此基礎上改變線速、note的page_index
		V2_data = chang_CHC_BPM(V2_data)

		# 進行錯誤偵測，並補上資料
		V2_data = click_error(V2_data)
		if V2_data["auto_fix_type"] == 1:
			V2_data = fix_hold_error(V2_data)  # 要改?

		C2_data = json.dumps(creat_C2(V2_data))
		C2_data = re.sub(' ', "", C2_data)
		C2_data2 = json.dumps(creat_C2V0plus(V2_data))
		C2_data2 = re.sub(' ', "", C2_data2)

		output_V1plus(V2_fliename, V2_data)
		result1 = creat_flie((V2_fliename + '.c2v0plus'), C2_data2)
		result2 = creat_flie((V2_fliename + '.c2v0'), C2_data)
		print(result1)
		print(result2)

# V2_text = get_V2_text(j)
# pprint(V2_data)
# pprint(get_V2_text(j))
