"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train.csv  --output_path=train.record
  # Create test data:
  python generate_tfrecord.py --csv_input=data/test.csv  --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('image_dir', '/home/local/3SI/andre.foote/Documents/AI\ML/Research/Data/CompCars/data/allimages', 'Path to images')
FLAGS = flags.FLAGS


#TO-DO place here the contents of conditionmap
def class_text_to_int(row_label):
	if row_label == "Audi A3 hatchback":
		return 1
	elif row_label == "Audi A4L":
		return 2
	elif row_label == "Audi A6L":
		return 3
	elif row_label == "Audi Q3":
		return 4
	elif row_label == "Audi Q5":
		return 5
	elif row_label == "Audi A6":
		return 6
	elif row_label == "Audi A3 sedan":
		return 7
	elif row_label == "Audi RS5":
		return 8
	elif row_label == "Audi RS7":
		return 9
	elif row_label == "Audi RS4":
		return 10
	elif row_label == "Audi RS Q3":
		return 11
	elif row_label == "Audi RS3":
		return 12
	elif row_label == "Audi TT RS":
		return 13
	elif row_label == "Audi RS6":
		return 14
	elif row_label == "Audi A1":
		return 15
	elif row_label == "Audi A4 estate":
		return 16
	elif row_label == "Audi A5 convertible":
		return 17
	elif row_label == "Audi A5 coupe":
		return 18
	elif row_label == "Audi A5 hatchback":
		return 19
	elif row_label == "Audi A6 hybrid":
		return 20
	elif row_label == "Audi A7":
		return 21
	elif row_label == "Audi A8L":
		return 22
	elif row_label == "Audi A8L hybrid":
		return 23
	elif row_label == "Audi Q5 hybrid":
		return 24
	elif row_label == "Audi Q7":
		return 25
	elif row_label == "Audi R8":
		return 26
	elif row_label == "Audi S5 convertible":
		return 27
	elif row_label == "Audi S5 coupe":
		return 28
	elif row_label == "Audi S5 hatchback":
		return 29
	elif row_label == "Audi S7":
		return 30
	elif row_label == "Audi S8":
		return 31
	elif row_label == "Audi SQ5":
		return 32
	elif row_label == "Audi TTS convertible":
		return 33
	elif row_label == "Audi TTS coupe":
		return 34
	elif row_label == "Audi TT convertible":
		return 35
	elif row_label == "Audi TT coupe":
		return 36
	elif row_label == "Audi A2":
		return 37
	elif row_label == "Audi quattro":
		return 38
	elif row_label == "Audi Urban":
		return 39
	elif row_label == "Audi Cross":
		return 40
	elif row_label == "Audi e-tron":
		return 41
	elif row_label == "Audi S3 hatchback":
		return 42
	elif row_label == "Audi R18":
		return 43
	elif row_label == "Audi A3 convertible":
		return 44
	elif row_label == "Audi A3 e-tron":
		return 45
	elif row_label == "Audi S1":
		return 46
	elif row_label == "Allroad":
		return 47
	elif row_label == "Crosslane Coupe":
		return 48
	elif row_label == "Audi S3 sedan":
		return 49
	elif row_label == "Audi S4":
		return 50
	elif row_label == "Nanuk":
		return 51
	elif row_label == "Audi TT offroad":
		return 52
	elif row_label == "Audi S3 convertible":
		return 53
	elif row_label == "BWM 3 Series":
		return 54
	elif row_label == "BWM X1":
		return 55
	elif row_label == "BWM 5 Series":
		return 56
	elif row_label == "BWM 1 Series M":
		return 57
	elif row_label == "BWM M3 coupe":
		return 58
	elif row_label == "BWM M3":
		return 59
	elif row_label == "BWM M4 coupe":
		return 60
	elif row_label == "BWM M5":
		return 61
	elif row_label == "BWM M6 coupe":
		return 62
	elif row_label == "BWM M6":
		return 63
	elif row_label == "BWM X5 M":
		return 64
	elif row_label == "BWM X6 M":
		return 65
	elif row_label == "BWM M3 convertible":
		return 66
	elif row_label == "BWM 1 Series convertible":
		return 67
	elif row_label == "BWM 1 Series couple":
		return 68
	elif row_label == "BWM 2 Series":
		return 69
	elif row_label == "BWM 3 Series GT":
		return 70
	elif row_label == "BWM 3 Series convertible":
		return 71
	elif row_label == "BWM 3 Series hybrid":
		return 72
	elif row_label == "BWM 3 Series estate":
		return 73
	elif row_label == "BWM 3 Series coupe":
		return 74
	elif row_label == "BWM 4 Series convertible":
		return 75
	elif row_label == "BWM 4 Series couple":
		return 76
	elif row_label == "BWM 4 Series":
		return 77
	elif row_label == "BWM 5 Series GT":
		return 78
	elif row_label == "BWM 5 Series hybrid":
		return 79
	elif row_label == "BWM 5 Series estate":
		return 80
	elif row_label == "BWM 6 Series convertible":
		return 81
	elif row_label == "BWM 6 Series couple":
		return 82
	elif row_label == "BWM 6 Series":
		return 83
	elif row_label == "BWM 7 Series":
		return 84
	elif row_label == "BWM 7 Series hybrid":
		return 85
	elif row_label == "BWM X3":
		return 86
	elif row_label == "BWM X4":
		return 87
	elif row_label == "BWM X5":
		return 88
	elif row_label == "BWM X6":
		return 89
	elif row_label == "BWM X6 Series hybrid":
		return 90
	elif row_label == "BWM Z4":
		return 91
	elif row_label == "BWM i3":
		return 92
	elif row_label == "BWM i8":
		return 93
	elif row_label == "ConnectedDrive":
		return 94
	elif row_label == "EfficientDynamics":
		return 95
	elif row_label == "Active Tourer":
		return 96
	elif row_label == "Isetta":
		return 97
	elif row_label == "BWM 1 Series hatchback":
		return 98
	elif row_label == "Zagato Coupe":
		return 99
	elif row_label == "Gran Lusso":
		return 100
	elif row_label == "BWM GINA":
		return 101
	elif row_label == "BWM 2 Series Active Tourer":
		return 102
	elif row_label == "Vision Future Luxury":
		return 103
	elif row_label == "Benz C Class":
		return 104
	elif row_label == "Benz C Class hybird":
		return 105
	elif row_label == "Benz GLK Class":
		return 106
	elif row_label == "Benz E Class":
		return 107
	elif row_label == "Benz A Class AMG":
		return 108
	elif row_label == "Benz CLS Class AMG":
		return 109
	elif row_label == "Benz C Class AMG":
		return 110
	elif row_label == "Benz GL Class AMG":
		return 111
	elif row_label == "Benz G Class AMG":
		return 112
	elif row_label == "Benz M Class AMG":
		return 113
	elif row_label == "Benz SLK Class AMG":
		return 114
	elif row_label == "Benz SLS Class AMG":
		return 115
	elif row_label == "Benz SL Class AMG":
		return 116
	elif row_label == "Benz S Class AMG":
		return 117
	elif row_label == "Benz E Class AMG":
		return 118
	elif row_label == "Benz CL Class AMG":
		return 119
	elif row_label == "Benz GLA Class AMG":
		return 120
	elif row_label == "Benz Vision AMG":
		return 121
	elif row_label == "AMG GT":
		return 122
	elif row_label == "Benz CLA Class AMG":
		return 123
	elif row_label == "Sprinter":
		return 124
	elif row_label == "Wei Yanuo":
		return 125
	elif row_label == "Wei Ting":
		return 126
	elif row_label == "Benz A Class":
		return 127
	elif row_label == "Benz CLA Class":
		return 128
	elif row_label == "Benz CLS Class":
		return 129
	elif row_label == "Benz CLS Class Shooting Brake":
		return 130
	elif row_label == "Benz C Class estate":
		return 131
	elif row_label == "Benz E Class convertible":
		return 132
	elif row_label == "Benz E Class couple":
		return 133
	elif row_label == "Benz GL Class":
		return 134
	elif row_label == "Benz G Class":
		return 135
	elif row_label == "Benz M Class":
		return 136
	elif row_label == "Benz R Class":
		return 137
	elif row_label == "Benz SLK Class":
		return 138
	elif row_label == "Benz SL Class":
		return 139
	elif row_label == "Benz S Class":
		return 140
	elif row_label == "Benz S Class hybird":
		return 141
	elif row_label == "Sprinter abroad version":
		return 142
	elif row_label == "Style Coupe":
		return 143
	elif row_label == "BlueZero":
		return 144
	elif row_label == "Benz Citan":
		return 145
	elif row_label == "Benz F800":
		return 146
	elif row_label == "Benz F125":
		return 147
	elif row_label == "Benz GLA Class":
		return 148
	elif row_label == "Benz E Class estate":
		return 149
	elif row_label == "Biome":
		return 150
	elif row_label == "Silver Arrow":
		return 151
	elif row_label == "Benz S Class coupe":
		return 152
	elif row_label == "Coupe SUV":
		return 153
	elif row_label == "Benz B Class":
		return 154
	elif row_label == "Ener-G-Force":
		return 155
	elif row_label == "Benz V Class":
		return 156
	elif row_label == "Unimog":
		return 157
	elif row_label == "encore":
		return 158
	elif row_label == "Buick GL8 Luxury Business":
		return 159
	elif row_label == "Buick GL8 Business":
		return 160
	elif row_label == "Regal":
		return 161
	elif row_label == "Regal GS":
		return 162
	elif row_label == "Lacrosse":
		return 163
	elif row_label == "Lacrosse eAssist":
		return 164
	elif row_label == "Exclle":
		return 165
	elif row_label == "Park Avenue":
		return 166
	elif row_label == "EXCELLE  GT":
		return 167
	elif row_label == "EXCELLE  XT":
		return 168
	elif row_label == "Buick Riviera":
		return 169
	elif row_label == "Envision":
		return 170
	elif row_label == "Enclave":
		return 171
	elif row_label == "Buick Encore":
		return 172
	elif row_label == "Buick Business":
		return 173
	elif row_label == "Buick Verano":
		return 174
	elif row_label == "Envision abroad version":
		return 175
	elif row_label == "Odyssey":
		return 176
	elif row_label == "City":
		return 177
	elif row_label == "Crosstour":
		return 178
	elif row_label == "Crider":
		return 179
	elif row_label == "Accord":
		return 180
	elif row_label == "Vezel":
		return 181
	elif row_label == "Fit":
		return 182
	elif row_label == "Honda CR-Z":
		return 183
	elif row_label == "Fit hybrid":
		return 184
	elif row_label == "Civic hybrid":
		return 185
	elif row_label == "Honda Legend":
		return 186
	elif row_label == "Honda S2000":
		return 187
	elif row_label == "Honda Urban":
		return 188
	elif row_label == "Honda Gear":
		return 189
	elif row_label == "Honda NSX":
		return 190
	elif row_label == "Honda CONCEPT M":
		return 191
	elif row_label == "Honda EV-Ster":
		return 192
	elif row_label == "Honda Ridgeline":
		return 193
	elif row_label == "Honda Step Bus":
		return 194
	elif row_label == "Honda AC-x":
		return 195
	elif row_label == "Honda FCX":
		return 196
	elif row_label == "Honda HSV-010 GT":
		return 197
	elif row_label == "Honda N BOX":
		return 198
	elif row_label == "Honda ONE":
		return 199
	elif row_label == "Honda P-NUT":
		return 200
	elif row_label == "Honda SUT":
		return 201
	elif row_label == "Honda Brio":
		return 202
	elif row_label == "Honda S660":
		return 203
	elif row_label == "Honda N-WGN":
		return 204
	elif row_label == "Honda HR-V":
		return 205
	elif row_label == "Honda Insight":
		return 206
	elif row_label == "Elysion":
		return 207
	elif row_label == "Jade":
		return 208
	elif row_label == "Spirior":
		return 209
	elif row_label == "Civic":
		return 210
	elif row_label == "Honda CR-V":
		return 211
	elif row_label == "CROSS 207":
		return 212
	elif row_label == "Peugeot 2008":
		return 213
	elif row_label == "Peugeot 207 hatchback":
		return 214
	elif row_label == "Peugeot 207 sedan":
		return 215
	elif row_label == "Peugeot 3008":
		return 216
	elif row_label == "Peugeot 301":
		return 217
	elif row_label == "Peugeot 307 hatchback":
		return 218
	elif row_label == "Peugeot 307 sedan":
		return 219
	elif row_label == "Peugeot 308":
		return 220
	elif row_label == "Peugeot 408":
		return 221
	elif row_label == "Peugeot 508":
		return 222
	elif row_label == "CROSS 307":
		return 223
	elif row_label == "Peugeot 207CC":
		return 224
	elif row_label == "Peugeot 308SW":
		return 225
	elif row_label == "Peugeot 4008":
		return 226
	elif row_label == "Peugeot RCZ":
		return 227
	elif row_label == "Peugeot 107":
		return 228
	elif row_label == "Peugeot 508 abroad version":
		return 229
	elif row_label == "Peugeot 208":
		return 230
	elif row_label == "Peugeot 308 abroad version":
		return 231
	elif row_label == "Urban Crossover":
		return 232
	elif row_label == "Peugeot 5008":
		return 233
	elif row_label == "Peugeot BB1":
		return 234
	elif row_label == "Peugeot EX1":
		return 235
	elif row_label == "Peugeot HR1":
		return 236
	elif row_label == "Peugeot HX1":
		return 237
	elif row_label == "Peugeot iON":
		return 238
	elif row_label == "Peugeot Onyx":
		return 239
	elif row_label == "Peugeot SR1":
		return 240
	elif row_label == "Peugeot SXC":
		return 241
	elif row_label == "Peugeot 108":
		return 242
	elif row_label == "EXALT":
		return 243
	elif row_label == "Peugeot 308CC":
		return 244
	elif row_label == "BYD F0":
		return 245
	elif row_label == "BYD F3DM":
		return 246
	elif row_label == "BYD F3R":
		return 247
	elif row_label == "BYD F6":
		return 248
	elif row_label == "BYD G3":
		return 249
	elif row_label == "BYD G3R":
		return 250
	elif row_label == "BYD G5":
		return 251
	elif row_label == "BYD G6":
		return 252
	elif row_label == "BYD L3":
		return 253
	elif row_label == "BYD M6":
		return 254
	elif row_label == "BYD S6":
		return 255
	elif row_label == "BYD S7":
		return 256
	elif row_label == "BYD e6":
		return 257
	elif row_label == "Qin":
		return 258
	elif row_label == "Si Rui":
		return 259
	elif row_label == "Su Rui":
		return 260
	elif row_label == "BYD F3":
		return 261
	elif row_label == "Boxster":
		return 262
	elif row_label == "Macan":
		return 263
	elif row_label == "Panamera":
		return 264
	elif row_label == "Panamera hybrid":
		return 265
	elif row_label == "Porsche 911":
		return 266
	elif row_label == "Porsche 918":
		return 267
	elif row_label == "Canyenne":
		return 268
	elif row_label == "Canyenne hybrid":
		return 269
	elif row_label == "Carrera GT":
		return 270
	elif row_label == "Porsche 917":
		return 271
	elif row_label == "Porsche 919":
		return 272
	elif row_label == "Cayman":
		return 273
	elif row_label == "BAW BJ40":
		return 274
	elif row_label == "BAW E Series sedan":
		return 275
	elif row_label == "BAW C60":
		return 276
	elif row_label == "BAW C71":
		return 277
	elif row_label == "BAW B61":
		return 278
	elif row_label == "BAW C30":
		return 279
	elif row_label == "BAW C90L":
		return 280
	elif row_label == "BAW C51X":
		return 281
	elif row_label == "BAW T60":
		return 282
	elif row_label == "concept500":
		return 283
	elif row_label == "concept900":
		return 284
	elif row_label == "BAW B90":
		return 285
	elif row_label == "BAW C50E":
		return 286
	elif row_label == "BAW E Series hatchback":
		return 287
	elif row_label == "Baojun 610":
		return 288
	elif row_label == "Baojun 630":
		return 289
	elif row_label == "Baojun 730":
		return 290
	elif row_label == "Lechi":
		return 291
	elif row_label == "Baojun 610 CROSS":
		return 292
	elif row_label == "Huansu S2":
		return 293
	elif row_label == "Huansu S3":
		return 294
	elif row_label == "Weiwang 205":
		return 295
	elif row_label == "Weiwang 307":
		return 296
	elif row_label == "Weiwang M20":
		return 297
	elif row_label == "Weiwang 306":
		return 298
	elif row_label == "BAW E150 EV":
		return 299
	elif row_label == "BJ212":
		return 300
	elif row_label == "Luba":
		return 301
	elif row_label == "Luling":
		return 302
	elif row_label == "Qishi":
		return 303
	elif row_label == "Ruiling":
		return 304
	elif row_label == "Yongshi":
		return 305
	elif row_label == "Yusheng 007":
		return 306
	elif row_label == "Yueling":
		return 307
	elif row_label == "Juedoushi":
		return 308
	elif row_label == "Besturn B50":
		return 309
	elif row_label == "Besturn B90":
		return 310
	elif row_label == "Besturn X80":
		return 311
	elif row_label == "Besturn B70":
		return 312
	elif row_label == "Flying Spur":
		return 313
	elif row_label == "Super Sport":
		return 314
	elif row_label == "Bentley Falcon":
		return 315
	elif row_label == "Brooklands":
		return 316
	elif row_label == "Arnage":
		return 317
	elif row_label == "Mulsanne":
		return 318
	elif row_label == "Veyron":
		return 319
	elif row_label == "Galibier":
		return 320
	elif row_label == "Great Wall C20R":
		return 321
	elif row_label == "Great Wall C50":
		return 322
	elif row_label == "Great Wall M1":
		return 323
	elif row_label == "Great Wall M2":
		return 324
	elif row_label == "Great Wall M4":
		return 325
	elif row_label == "Great Wall V80":
		return 326
	elif row_label == "Wingle 3":
		return 327
	elif row_label == "Wingle 5":
		return 328
	elif row_label == "Wingle 6":
		return 329
	elif row_label == "Jindier":
		return 330
	elif row_label == "Jingling":
		return 331
	elif row_label == "Kuxiong":
		return 332
	elif row_label == "Lingao":
		return 333
	elif row_label == "Xuanli":
		return 334
	elif row_label == "Xuanli CROSS":
		return 335
	elif row_label == "Oula":
		return 336
	elif row_label == "Great Wall C70":
		return 337
	elif row_label == "Great Wall C30":
		return 338
	elif row_label == "Benben":
		return 339
	elif row_label == "Benben MINI":
		return 340
	elif row_label == "Changan CS35":
		return 341
	elif row_label == "Changan CS75":
		return 342
	elif row_label == "Changan CX20":
		return 343
	elif row_label == "Changan CS30 hatchback":
		return 344
	elif row_label == "Changan CS30 sedan":
		return 345
	elif row_label == "Yidong":
		return 346
	elif row_label == "Yuexiang V3":
		return 347
	elif row_label == "Yuexiang V5":
		return 348
	elif row_label == "Yuexiang hatchback":
		return 349
	elif row_label == "Yuexiang sedan":
		return 350
	elif row_label == "Zhishang XT":
		return 351
	elif row_label == "Ruiping":
		return 352
	elif row_label == "Zhixiang":
		return 353
	elif row_label == "Changan SENSE":
		return 354
	elif row_label == "Changan CS95":
		return 355
	elif row_label == "Changan VOSS":
		return 356
	elif row_label == "Benben LOVE":
		return 357
	elif row_label == "Changan Ounuo":
		return 358
	elif row_label == "Changan Xiaoka":
		return 359
	elif row_label == "Changan Xingka":
		return 360
	elif row_label == "Changan Star":
		return 361
	elif row_label == "Changan Star 7":
		return 362
	elif row_label == "Changan Star S460":
		return 363
	elif row_label == "Oulove":
		return 364
	elif row_label == "Zunxing":
		return 365
	elif row_label == "Ruixing":
		return 366
	elif row_label == "Changan Shenqi":
		return 367
	elif row_label == "Ideal":
		return 368
	elif row_label == "Funyun":
		return 369
	elif row_label == "Furuida":
		return 370
	elif row_label == "Cross Polo":
		return 371
	elif row_label == "Polo hatchback":
		return 372
	elif row_label == "Polo sedan":
		return 373
	elif row_label == "GOL":
		return 374
	elif row_label == "Cross Lavida":
		return 375
	elif row_label == "Gran Lavida":
		return 376
	elif row_label == "Lavide":
		return 377
	elif row_label == "Passat":
		return 378
	elif row_label == "Passat Lingyu":
		return 379
	elif row_label == "Santana":
		return 380
	elif row_label == "Santana Vista":
		return 381
	elif row_label == "Touran":
		return 382
	elif row_label == "Tiguan":
		return 383
	elif row_label == "NMC":
		return 384
	elif row_label == "Polo GTI":
		return 385
	elif row_label == "Cross Golf":
		return 386
	elif row_label == "Volkswagen Eos":
		return 387
	elif row_label == "Volkswagen R36":
		return 388
	elif row_label == "Golf GTI convertible":
		return 389
	elif row_label == "Golf R":
		return 390
	elif row_label == "Golf R convertible":
		return 391
	elif row_label == "Golf convertible":
		return 392
	elif row_label == "Golf estate":
		return 393
	elif row_label == "Phaeton":
		return 394
	elif row_label == "Beetle":
		return 395
	elif row_label == "Caravelle":
		return 396
	elif row_label == "Multivan":
		return 397
	elif row_label == "Magotan estate":
		return 398
	elif row_label == "Scirocco":
		return 399
	elif row_label == "Scirocco R":
		return 400
	elif row_label == "Touareg":
		return 401
	elif row_label == "Touareg hybrid":
		return 402
	elif row_label == "Sharan":
		return 403
	elif row_label == "Polo abroad version":
		return 404
	elif row_label == "BlueSport":
		return 405
	elif row_label == "Beetle convertible":
		return 406
	elif row_label == "Variant":
		return 407
	elif row_label == "Amarok Pickup":
		return 408
	elif row_label == "Cross Coupe":
		return 409
	elif row_label == "E-Bugster":
		return 410
	elif row_label == "Passat abroad version":
		return 411
	elif row_label == "CrossBlue":
		return 412
	elif row_label == "Volkswagen XL1":
		return 413
	elif row_label == "Bulli":
		return 414
	elif row_label == "Buggy Up":
		return 415
	elif row_label == "Jetta abroad version":
		return 416
	elif row_label == "New Compact":
		return 417
	elif row_label == "Routan":
		return 418
	elif row_label == "Taigun":
		return 419
	elif row_label == "Volkswagen  Up!Lite":
		return 420
	elif row_label == "T-ROC":
		return 421
	elif row_label == "Tiguan abroad version":
		return 422
	elif row_label == "e-Co-Motion":
		return 423
	elif row_label == "Milano":
		return 424
	elif row_label == "Nils":
		return 425
	elif row_label == "Space Up":
		return 426
	elif row_label == "Volkswagen up":
		return 427
	elif row_label == "Volkswagen Fox":
		return 428
	elif row_label == "Caddy abroad version":
		return 429
	elif row_label == "Bora":
		return 430
	elif row_label == "Golf":
		return 431
	elif row_label == "Golf GTI":
		return 432
	elif row_label == "Jetta":
		return 433
	elif row_label == "Magotan":
		return 434
	elif row_label == "Sagitar":
		return 435
	elif row_label == "Sagitar GLI":
		return 436
	elif row_label == "Volkswagen CC":
		return 437
	elif row_label == "DS 5":
		return 438
	elif row_label == "DS 6":
		return 439
	elif row_label == "DS 5LS":
		return 440
	elif row_label == "DS 3":
		return 441
	elif row_label == "DS Wild Rubis":
		return 442
	elif row_label == "DS 9":
		return 443
	elif row_label == "DS 4":
		return 444
	elif row_label == "Ram":
		return 445
	elif row_label == "Journey":
		return 446
	elif row_label == "Challenger":
		return 447
	elif row_label == "Durango":
		return 448
	elif row_label == "Avenger":
		return 449
	elif row_label == "Dart":
		return 450
	elif row_label == "Charger":
		return 451
	elif row_label == "Viper":
		return 452
	elif row_label == "Circuit EV":
		return 453
	elif row_label == "Rampage":
		return 454
	elif row_label == "Dodge M80":
		return 455
	elif row_label == "Nitro":
		return 456
	elif row_label == "Charger SRT":
		return 457
	elif row_label == "Challenger SRT":
		return 458
	elif row_label == "Viper SRT":
		return 459
	elif row_label == "Caliber":
		return 460
	elif row_label == "V3 Lingyue":
		return 461
	elif row_label == "V6 Lingyue":
		return 462
	elif row_label == "Delica":
		return 463
	elif row_label == "Xiwang":
		return 464
	elif row_label == "Northeast V4":
		return 465
	elif row_label == "Northeast V7":
		return 466
	elif row_label == "V5 Lingzhi":
		return 467
	elif row_label == "Junfeng CV03":
		return 468
	elif row_label == "Dongfeng HUV":
		return 469
	elif row_label == "Yufeng":
		return 470
	elif row_label == "Fengxing CM7":
		return 471
	elif row_label == "Jingyi S50":
		return 472
	elif row_label == "Jingyi SUV":
		return 473
	elif row_label == "Jingyi X3":
		return 474
	elif row_label == "Jingyi X5":
		return 475
	elif row_label == "Lingzhi":
		return 476
	elif row_label == "Jingyi":
		return 477
	elif row_label == "Fengshen A30":
		return 478
	elif row_label == "Fengshen CROSS":
		return 479
	elif row_label == "Fengshen H30":
		return 480
	elif row_label == "Fengshen S30":
		return 481
	elif row_label == "Fengshen E30L":
		return 482
	elif row_label == "Fengshen A60":
		return 483
	elif row_label == "Ruiqi Pickup":
		return 484
	elif row_label == "Ruiqi Cargo":
		return 485
	elif row_label == "Shuaike":
		return 486
	elif row_label == "Yuxuan":
		return 487
	elif row_label == "Junfeng":
		return 488
	elif row_label == "DFSK C37":
		return 489
	elif row_label == "DFSK K07":
		return 490
	elif row_label == "DFSK K07II":
		return 491
	elif row_label == "DFSK V07S":
		return 492
	elif row_label == "DFSK V21":
		return 493
	elif row_label == "DFSK V27":
		return 494
	elif row_label == "DFSK V29":
		return 495
	elif row_label == "Fengguang":
		return 496
	elif row_label == "DFSK V22":
		return 497
	elif row_label == "escort":
		return 498
	elif row_label == "Fiesta sedan":
		return 499
	elif row_label == "Classic Focus hatchback":
		return 500
	elif row_label == "Classic Focus sedan":
		return 501
	elif row_label == "S-MAX":
		return 502
	elif row_label == "New Focus hatchback":
		return 503
	elif row_label == "New Focus sedan":
		return 504
	elif row_label == "Ecosport":
		return 505
	elif row_label == "Kuga":
		return 506
	elif row_label == "Mendeo Zhisheng":
		return 507
	elif row_label == "Mendeo":
		return 508
	elif row_label == "Fiesta hatchback":
		return 509
	elif row_label == "Transit":
		return 510
	elif row_label == "Focus ST":
		return 511
	elif row_label == "Ford F-150":
		return 512
	elif row_label == "Ford F-250":
		return 513
	elif row_label == "Ford F-350":
		return 514
	elif row_label == "Ford F-650":
		return 515
	elif row_label == "Fiesta ST":
		return 516
	elif row_label == "Edge":
		return 517
	elif row_label == "Explorer":
		return 518
	elif row_label == "Mustang":
		return 519
	elif row_label == "Ford Ka":
		return 520
	elif row_label == "Ford Flex":
		return 521
	elif row_label == "Ford iosis max":
		return 522
	elif row_label == "Ford Taurus":
		return 523
	elif row_label == "Ford Fusion":
		return 524
	elif row_label == "Atlas":
		return 525
	elif row_label == "Ford Transit":
		return 526
	elif row_label == "Ford B-MAX":
		return 527
	elif row_label == "Ford C-MAX":
		return 528
	elif row_label == "Escort":
		return 529
	elif row_label == "Airstream":
		return 530
	elif row_label == "Falcon":
		return 531
	elif row_label == "Galaxy":
		return 532
	elif row_label == "Ranger":
		return 533
	elif row_label == "Territory":
		return 534
	elif row_label == "Tourneo Courier":
		return 535
	elif row_label == "Tourneo Custom":
		return 536
	elif row_label == "Vertrek":
		return 537
	elif row_label == "Ford Evos":
		return 538
	elif row_label == "S-MAX abroad version":
		return 539
	elif row_label == "Fiesta abroad version":
		return 540
	elif row_label == "Expedition":
		return 541
	elif row_label == "Super Duty":
		return 542
	elif row_label == "Focus abroad version":
		return 543
	elif row_label == "Troller":
		return 544
	elif row_label == "Ford E":
		return 545
	elif row_label == "Formula":
		return 546
	elif row_label == "Taurus":
		return 547
	elif row_label == "Feixiang":
		return 548
	elif row_label == "Zhiyue":
		return 549
	elif row_label == "Palio":
		return 550
	elif row_label == "Bravo":
		return 551
	elif row_label == "FIAT 500C":
		return 552
	elif row_label == "Freemont":
		return 553
	elif row_label == "Linea":
		return 554
	elif row_label == "Punto":
		return 555
	elif row_label == "FIAT Fiorino Qubo":
		return 556
	elif row_label == "Doblo":
		return 557
	elif row_label == "FIAT 500L":
		return 558
	elif row_label == "FIAT Idea":
		return 559
	elif row_label == "FIAT Panda":
		return 560
	elif row_label == "FIAT Strada":
		return 561
	elif row_label == "FIAT Uno":
		return 562
	elif row_label == "FIAT 126P":
		return 563
	elif row_label == "FIAT 500":
		return 564
	elif row_label == "California":
		return 565
	elif row_label == "Ferrari 458":
		return 566
	elif row_label == "Ferrari 599":
		return 567
	elif row_label == "Ferrari FF":
		return 568
	elif row_label == "LaFerrari":
		return 569
	elif row_label == "Sergio":
		return 570
	elif row_label == "F12berlinetta":
		return 571
	elif row_label == "Qiteng M70":
		return 572
	elif row_label == "Chuanqi GA3":
		return 573
	elif row_label == "Chuanqi GA5":
		return 574
	elif row_label == "Chuanqi GS5":
		return 575
	elif row_label == "E-jet":
		return 576
	elif row_label == "e-linker":
		return 577
	elif row_label == "Cabrio-Coupe":
		return 578
	elif row_label == "Trumpchi GA3S horizon":
		return 579
	elif row_label == "GMC3500":
		return 580
	elif row_label == "Yukon":
		return 581
	elif row_label == "Terrain":
		return 582
	elif row_label == "Sierra":
		return 583
	elif row_label == "Acadia":
		return 584
	elif row_label == "GMC CANYON":
		return 585
	elif row_label == "Savana":
		return 586
	elif row_label == "Haval H3":
		return 587
	elif row_label == "Haval H5":
		return 588
	elif row_label == "Haval H6":
		return 589
	elif row_label == "Haval H8":
		return 590
	elif row_label == "Haval ?":
		return 591
	elif row_label == "Haval IF":
		return 592
	elif row_label == "Haval H7":
		return 593
	elif row_label == "Haval E":
		return 594
	elif row_label == "Haval H2":
		return 595
	elif row_label == "FOS":
		return 596
	elif row_label == "Haima Prince":
		return 597
	elif row_label == "Haima Me":
		return 598
	elif row_label == "Haima C2":
		return 599
	elif row_label == "Haima C3":
		return 600
	elif row_label == "Baimawangzi":
		return 601
	elif row_label == "Qiangwawangzi":
		return 602
	elif row_label == "Haimaaishang":
		return 603
	elif row_label == "Junyi":
		return 604
	elif row_label == "Zunludabawang":
		return 605
	elif row_label == "Zunluxiaobawang":
		return 606
	elif row_label == "Minyi":
		return 607
	elif row_label == "Saima":
		return 608
	elif row_label == "Zhongyi V5":
		return 609
	elif row_label == "Lubao":
		return 610
	elif row_label == "Aolong":
		return 611
	elif row_label == "Dachaishen":
		return 612
	elif row_label == "Huanghai N1":
		return 613
	elif row_label == "Huanghai Challenger":
		return 614
	elif row_label == "Qisheng F1":
		return 615
	elif row_label == "Qisheng V3":
		return 616
	elif row_label == "Ruitu":
		return 617
	elif row_label == "Xiaochaishen":
		return 618
	elif row_label == "Aojun":
		return 619
	elif row_label == "Tuteng T1":
		return 620
	elif row_label == "Tuteng T3":
		return 621
	elif row_label == "Tuteng T2":
		return 622
	elif row_label == "Haige H5C":
		return 623
	elif row_label == "Longwei":
		return 624
	elif row_label == "Yujun":
		return 625
	elif row_label == "Haige H5V":
		return 626
	elif row_label == "Grand Cherokee SRT":
		return 627
	elif row_label == "Wrangler":
		return 628
	elif row_label == "Compass":
		return 629
	elif row_label == "Cherokee":
		return 630
	elif row_label == "Patriot":
		return 631
	elif row_label == "Free":
		return 632
	elif row_label == "Jeep J12":
		return 633
	elif row_label == "Renegade":
		return 634
	elif row_label == "Grand Cherokee":
		return 635
	elif row_label == "Gaguar F-TYPE":
		return 636
	elif row_label == "Gaguar XJ":
		return 637
	elif row_label == "Gaguar XK":
		return 638
	elif row_label == "Gaguar C-X75":
		return 639
	elif row_label == "Gaguar C-TYPE":
		return 640
	elif row_label == "Gaguar E-TYPE":
		return 641
	elif row_label == "Gaguar C-X17":
		return 642
	elif row_label == "Gaguar XE":
		return 643
	elif row_label == "Gaguar XF":
		return 644
	elif row_label == "Aifei":
		return 645
	elif row_label == "Jiulong A5":
		return 646
	elif row_label == "Jiulong A6":
		return 647
	elif row_label == "Big MPV":
		return 648
	elif row_label == "Seville SLS":
		return 649
	elif row_label == "Cadillac XTS":
		return 650
	elif row_label == "Cadillac CTS":
		return 651
	elif row_label == "Cadillac ATS-L":
		return 652
	elif row_label == "Cadillac ATS":
		return 653
	elif row_label == "Cadillac SRX":
		return 654
	elif row_label == "Escalade":
		return 655
	elif row_label == "Escalade hybrid":
		return 656
	elif row_label == "Cadillac BLS":
		return 657
	elif row_label == "Cadillac ELR":
		return 658
	elif row_label == "Cadillac Ciel":
		return 659
	elif row_label == "Elmiraj":
		return 660
	elif row_label == "Koenigsegg Agera":
		return 661
	elif row_label == "Koenigsegg CCR":
		return 662
	elif row_label == "One_1":
		return 663
	elif row_label == "Koenigsegg CCXR":
		return 664
	elif row_label == "Renault Scenic":
		return 665
	elif row_label == "Wind Lang":
		return 666
	elif row_label == "Koleos":
		return 667
	elif row_label == "Laguna":
		return 668
	elif row_label == "Laguna Gu Bbe":
		return 669
	elif row_label == "Megan Aa":
		return 670
	elif row_label == "Tower Siman":
		return 671
	elif row_label == "Latitude":
		return 672
	elif row_label == "Cleo":
		return 673
	elif row_label == "Reno Wind":
		return 674
	elif row_label == "Reno Captur":
		return 675
	elif row_label == "Reno Frendzy":
		return 676
	elif row_label == "Reno ZOE":
		return 677
	elif row_label == "Reno Twizy":
		return 678
	elif row_label == "Reno Symbol":
		return 679
	elif row_label == "Reno R-Space":
		return 680
	elif row_label == "Reno Twingo":
		return 681
	elif row_label == "Reno Alpine":
		return 682
	elif row_label == "Reno Twin-Run":
		return 683
	elif row_label == "Reno Twin-Z":
		return 684
	elif row_label == "Reno Kwid":
		return 685
	elif row_label == "Scenic":
		return 686
	elif row_label == "Fshion":
		return 687
	elif row_label == "Landwind X8":
		return 688
	elif row_label == "Landwind X5":
		return 689
	elif row_label == "Lincoln MKS":
		return 690
	elif row_label == "Lincoln MKT":
		return 691
	elif row_label == "Lincoln MKX":
		return 692
	elif row_label == "Lincoln MKZ":
		return 693
	elif row_label == "Navigator":
		return 694
	elif row_label == "Lincoln MKC":
		return 695
	elif row_label == "Lorinser M Class":
		return 696
	elif row_label == "Lorinser S Class":
		return 697
	elif row_label == "Lorinser C Class":
		return 698
	elif row_label == "Lorinser G Class":
		return 699
	elif row_label == "Lorinser E Class":
		return 700
	elif row_label == "MINI":
		return 701
	elif row_label == "MINI CLUBMAN":
		return 702
	elif row_label == "MINI COUNTRYMAN":
		return 703
	elif row_label == "MINI COUPE":
		return 704
	elif row_label == "MINI PACEMAN":
		return 705
	elif row_label == "MINI ROADSTER":
		return 706
	elif row_label == "MINI E":
		return 707
	elif row_label == "MINI CLUBVAN":
		return 708
	elif row_label == "MINI BEACHCOMBER":
		return 709
	elif row_label == "MINI VISION":
		return 710
	elif row_label == "MINI Superleggera":
		return 711
	elif row_label == "MINI CABRIO":
		return 712
	elif row_label == "MINI JCW":
		return 713
	elif row_label == "MINI JCW COUNTRYMAN":
		return 714
	elif row_label == "MINI JCW COUPE":
		return 715
	elif row_label == "MINI JCW PACEMAN":
		return 716
	elif row_label == "Morgan Plus 8":
		return 717
	elif row_label == "Morgan 4-4":
		return 718
	elif row_label == "Morgan Aero":
		return 719
	elif row_label == "Oley hatchback":
		return 720
	elif row_label == "Oley sedan":
		return 721
	elif row_label == "Murano":
		return 722
	elif row_label == "X-Trail":
		return 723
	elif row_label == "Teana":
		return 724
	elif row_label == "New Sylphy":
		return 725
	elif row_label == "Sylphy":
		return 726
	elif row_label == "Sunshine":
		return 727
	elif row_label == "Yida":
		return 728
	elif row_label == "Qashqai":
		return 729
	elif row_label == "Livina":
		return 730
	elif row_label == "Tiida":
		return 731
	elif row_label == "Ma Chi":
		return 732
	elif row_label == "Paladin":
		return 733
	elif row_label == "Nissan D22 Pickup":
		return 734
	elif row_label == "Nissan D22 Cargo":
		return 735
	elif row_label == "Nissan NV200":
		return 736
	elif row_label == "Palazzi":
		return 737
	elif row_label == "Bilian":
		return 738
	elif row_label == "Nissan 370Z":
		return 739
	elif row_label == "Nissan GT-R":
		return 740
	elif row_label == "Nissan Juke":
		return 741
	elif row_label == "Patrol":
		return 742
	elif row_label == "Nissan Cube":
		return 743
	elif row_label == "Nissan NUVU":
		return 744
	elif row_label == "Leaf":
		return 745
	elif row_label == "Pathfinder":
		return 746
	elif row_label == "Versa":
		return 747
	elif row_label == "Resonance":
		return 748
	elif row_label == "Friend-ME":
		return 749
	elif row_label == "Extrem":
		return 750
	elif row_label == "DeltaWing":
		return 751
	elif row_label == "Frontier":
		return 752
	elif row_label == "Hi-Cross":
		return 753
	elif row_label == "Invitation":
		return 754
	elif row_label == "Sentra":
		return 755
	elif row_label == "Terra":
		return 756
	elif row_label == "Titan":
		return 757
	elif row_label == "Nissan NV3500":
		return 758
	elif row_label == "Armada":
		return 759
	elif row_label == "Rogue":
		return 760
	elif row_label == "BladeGlider":
		return 761
	elif row_label == "Sports Sedan":
		return 762
	elif row_label == "Pulsar":
		return 763
	elif row_label == "2021 Vision Gran Turismo":
		return 764
	elif row_label == "Quest":
		return 765
	elif row_label == "IDX":
		return 766
	elif row_label == "Lannia Concept":
		return 767
	elif row_label == "Navara":
		return 768
	elif row_label == "Altima":
		return 769
	elif row_label == "Fabia":
		return 770
	elif row_label == "Octavia":
		return 771
	elif row_label == "Octavia RS":
		return 772
	elif row_label == "Superb":
		return 773
	elif row_label == "Yeti":
		return 774
	elif row_label == "Haorui":
		return 775
	elif row_label == "Rapid Spaceback":
		return 776
	elif row_label == "Rapid":
		return 777
	elif row_label == "Fabia Scout":
		return 778
	elif row_label == "Yeti abroad version":
		return 779
	elif row_label == "Citigo":
		return 780
	elif row_label == "Mission L":
		return 781
	elif row_label == "Roomster":
		return 782
	elif row_label == "Octavia abroad version":
		return 783
	elif row_label == "Octavia RS abroad version":
		return 784
	elif row_label == "Vision D":
		return 785
	elif row_label == "VisionC":
		return 786
	elif row_label == "CitiJet":
		return 787
	elif row_label == "Superb Derivative":
		return 788
	elif row_label == "Actyon":
		return 789
	elif row_label == "Rexton":
		return 790
	elif row_label == "Rexton W":
		return 791
	elif row_label == "Rodius":
		return 792
	elif row_label == "Kyron":
		return 793
	elif row_label == "Chairman":
		return 794
	elif row_label == "Ssang Yong XIV-2":
		return 795
	elif row_label == "Ssang Yong e-XIV":
		return 796
	elif row_label == "Ssang Yong SIV-1":
		return 797
	elif row_label == "Ssang Yong XIV-1":
		return 798
	elif row_label == "Ssang Yong XIV":
		return 799
	elif row_label == "Korando":
		return 800
	elif row_label == "SAAB 95":
		return 801
	elif row_label == "SAAB 9X":
		return 802
	elif row_label == "MODEL S":
		return 803
	elif row_label == "TESLA Roadster":
		return 804
	elif row_label == "MODEL X":
		return 805
	elif row_label == "WeaLink H3":
		return 806
	elif row_label == "WeaLink V5":
		return 807
	elif row_label == "WeaLink X5":
		return 808
	elif row_label == "i30":
		return 809
	elif row_label == "ix35":
		return 810
	elif row_label == "Avante":
		return 811
	elif row_label == "Sonata":
		return 812
	elif row_label == "Mistra":
		return 813
	elif row_label == "Moinca":
		return 814
	elif row_label == "Santafe":
		return 815
	elif row_label == "Rena":
		return 816
	elif row_label == "Verna":
		return 817
	elif row_label == "Sonata 8":
		return 818
	elif row_label == "Tucson":
		return 819
	elif row_label == "Accent":
		return 820
	elif row_label == "Elantra":
		return 821
	elif row_label == "Elantra Yuedong":
		return 822
	elif row_label == "ix25":
		return 823
	elif row_label == "Sonata hybrid":
		return 824
	elif row_label == "Grand SantaFe":
		return 825
	elif row_label == "Wagon":
		return 826
	elif row_label == "Genesis":
		return 827
	elif row_label == "Rohens":
		return 828
	elif row_label == "Rohens Coupe":
		return 829
	elif row_label == "Veracruz":
		return 830
	elif row_label == "Equus":
		return 831
	elif row_label == "Grandeur":
		return 832
	elif row_label == "i20":
		return 833
	elif row_label == "Tucson abroad vresion":
		return 834
	elif row_label == "i40":
		return 835
	elif row_label == "Hyundai i-oniq":
		return 836
	elif row_label == "i10":
		return 837
	elif row_label == "Hyundai HB20":
		return 838
	elif row_label == "Hyundai HND-9":
		return 839
	elif row_label == "Blue2":
		return 840
	elif row_label == "Curb":
		return 841
	elif row_label == "Hexa Space":
		return 842
	elif row_label == "Nuvis":
		return 843
	elif row_label == "ix20":
		return 844
	elif row_label == "Hyundai RB":
		return 845
	elif row_label == "Sonata abroad version":
		return 846
	elif row_label == "Accent abroad version":
		return 847
	elif row_label == "Elantra abroad version":
		return 848
	elif row_label == "Intrado":
		return 849
	elif row_label == "Veloster":
		return 850
	elif row_label == "ESQ":
		return 851
	elif row_label == "Infiniti Q50":
		return 852
	elif row_label == "Infiniti Q50 hybrid":
		return 853
	elif row_label == "Infiniti Q60":
		return 854
	elif row_label == "Infiniti Q60S":
		return 855
	elif row_label == "Infiniti Q70L":
		return 856
	elif row_label == "Infiniti Q70L hybrid":
		return 857
	elif row_label == "Infiniti QX50":
		return 858
	elif row_label == "Infiniti QX60":
		return 859
	elif row_label == "Infiniti Q60 hybrid":
		return 860
	elif row_label == "Infiniti QX70":
		return 861
	elif row_label == "Infiniti QX80":
		return 862
	elif row_label == "Essence":
		return 863
	elif row_label == "Emerg-E":
		return 864
	elif row_label == "Etherea":
		return 865
	elif row_label == "Infiniti LE":
		return 866
	elif row_label == "Infiniti Q30":
		return 867
	elif row_label == "Infiniti Q40":
		return 868
	elif row_label == "Infiniti G Class":
		return 869
	elif row_label == "Infiniti Q50L":
		return 870
	elif row_label == "Jiangnan TT":
		return 871
	elif row_label == "Zotye 5008":
		return 872
	elif row_label == "Zotye M300":
		return 873
	elif row_label == "Zotye T200":
		return 874
	elif row_label == "Zotye T600":
		return 875
	elif row_label == "Zotye V10":
		return 876
	elif row_label == "Zotye Z100":
		return 877
	elif row_label == "Zotye Z200":
		return 878
	elif row_label == "Zotye Z200HB":
		return 879
	elif row_label == "Zotye Z300":
		return 880
	elif row_label == "Zhidou E20":
		return 881
	elif row_label == "Dokker":
		return 882
	elif row_label == "Duster":
		return 883
	elif row_label == "Logan":
		return 884
	elif row_label == "Sandero":
		return 885
	elif row_label == "Lodgy":
		return 886
	elif row_label == "Ranz":
		return 887
	elif row_label == "Apollo":
		return 888
	elif row_label == "Explosion":
		return 889
	elif row_label == "Tornante":
		return 890
	elif row_label == "CEVENNES":
		return 891
	elif row_label == "HEMERA":
		return 892
	elif row_label == "DB9":
		return 893
	elif row_label == "Rapide":
		return 894
	elif row_label == "V12 Vantage":
		return 895
	elif row_label == "V8 Vantage":
		return 896
	elif row_label == "Vanquish":
		return 897
	elif row_label == "Virage":
		return 898
	elif row_label == "Zagato":
		return 899
	elif row_label == "ONE-77":
		return 900
	elif row_label == "Cygnet":
		return 901
	elif row_label == "Lagonda":
		return 902
	elif row_label == "CC100":
		return 903
	elif row_label == "DB5":
		return 904
	elif row_label == "DBS":
		return 905
	elif row_label == "Junpai D60":
		return 906
	elif row_label == "Weizhi":
		return 907
	elif row_label == "Weizhi V2":
		return 908
	elif row_label == "Weizhi V2 CROSS":
		return 909
	elif row_label == "Weizhi V5":
		return 910
	elif row_label == "Weizi":
		return 911
	elif row_label == "Xiali N5":
		return 912
	elif row_label == "Xiali N7":
		return 913
	elif row_label == "Xiali hatchback":
		return 914
	elif row_label == "Xiali sedan":
		return 915
	elif row_label == "FAW NH2":
		return 916
	elif row_label == "FAW NS2":
		return 917
	elif row_label == "FAW TFC":
		return 918
	elif row_label == "FAW X121":
		return 919
	elif row_label == "Kuncheng":
		return 920
	elif row_label == "Jiabao T50":
		return 921
	elif row_label == "Jiabao T57":
		return 922
	elif row_label == "Jiabao V52":
		return 923
	elif row_label == "Jiabao V55":
		return 924
	elif row_label == "Jiabao V70":
		return 925
	elif row_label == "Jiabao V80":
		return 926
	elif row_label == "Senya M80":
		return 927
	elif row_label == "Senya S80":
		return 928
	elif row_label == "Jiabao T51":
		return 929
	elif row_label == "Zhinuo 1E":
		return 930
	elif row_label == "Vauxhall Antara":
		return 931
	elif row_label == "Vauxhall Adam":
		return 932
	elif row_label == "Vauxhall Cascada":
		return 933
	elif row_label == "Vauxhall Corsa":
		return 934
	elif row_label == "Vauxhall Insignia":
		return 935
	elif row_label == "Vauxhall Meriva":
		return 936
	elif row_label == "Vauxhall Mokka":
		return 937
	elif row_label == "Vauxhall VXR8":
		return 938
	elif row_label == "Vauxhall Astra":
		return 939
	elif row_label == "ABT A3":
		return 940
	elif row_label == "ABT A4":
		return 941
	elif row_label == "ABT A5":
		return 942
	elif row_label == "ABT A8":
		return 943
	elif row_label == "ABT A6":
		return 944
	elif row_label == "ABT Q7":
		return 945
	elif row_label == "ABT TT":
		return 946
	elif row_label == "ABT A7":
		return 947
	elif row_label == "ABT Q3":
		return 948
	elif row_label == "ABT Q5":
		return 949
	elif row_label == "ABT RS 4":
		return 950
	elif row_label == "ABT A1":
		return 951
	elif row_label == "Venom GT":
		return 952
	elif row_label == "Venom F5":
		return 953
	elif row_label == "VelociRaptor":
		return 954
	elif row_label == "Tuatara":
		return 955
	elif row_label == "Ultimate":
		return 956
	elif row_label == "Town":
		return 957
	elif row_label == "Chrysler  200C":
		return 958
	elif row_label == "Chrysler  Sebring":
		return 959
	elif row_label == "Prowler":
		return 960
	elif row_label == "Chrysler 200":
		return 961
	elif row_label == "Chrysler Delta":
		return 962
	elif row_label == "Chrysler Ypsilon":
		return 963
	elif row_label == "Chrysler 700C":
		return 964
	elif row_label == "Chrysler 300C SRT":
		return 965
	elif row_label == "Chrysler 300C":
		return 966
	elif row_label == "Grand Voager":
		return 967
	elif row_label == "Discovery":
		return 968
	elif row_label == "Range Rover":
		return 969
	elif row_label == "Range Rover hybrid":
		return 970
	elif row_label == "Evoque":
		return 971
	elif row_label == "Range Rover Sport":
		return 972
	elif row_label == "Freelander":
		return 973
	elif row_label == "Defender":
		return 974
	elif row_label == "Land Rover DC100":
		return 975
	elif row_label == "?Vision":
		return 976
	elif row_label == "Feiling Pickup":
		return 977
	elif row_label == "Feiteng C5":
		return 978
	elif row_label == "Cheetah CS6":
		return 979
	elif row_label == "Cheetah CS7":
		return 980
	elif row_label == "Cheetah Q6":
		return 981
	elif row_label == "Feiteng":
		return 982
	elif row_label == "Aventador":
		return 983
	elif row_label == "Reventon":
		return 984
	elif row_label == "Insecta":
		return 985
	elif row_label == "Estoque":
		return 986
	elif row_label == "Gallardo":
		return 987
	elif row_label == "Urus":
		return 988
	elif row_label == "Veneno":
		return 989
	elif row_label == "Egoista":
		return 990
	elif row_label == "5-95 Zagato":
		return 991
	elif row_label == "Huracan":
		return 992
	elif row_label == "Ghibli":
		return 993
	elif row_label == "Quattroporte":
		return 994
	elif row_label == "GranCabrio":
		return 995
	elif row_label == "Levante":
		return 996
	elif row_label == "Alfieri":
		return 997
	elif row_label == "Maserati GT":
		return 998
	elif row_label == "MASTER CEO":
		return 999
	elif row_label == "7 SUV":
		return 1000
	elif row_label == "Luxgen 5 Sedan":
		return 1001
	elif row_label == "You 6 SUV":
		return 1002
	elif row_label == "7 MPV":
		return 1003
	elif row_label == "Forte":
		return 1004
	elif row_label == "KIA K2 sedan":
		return 1005
	elif row_label == "KIA K3":
		return 1006
	elif row_label == "KIA K3S":
		return 1007
	elif row_label == "KIA K4":
		return 1008
	elif row_label == "KIA K5":
		return 1009
	elif row_label == "RIO":
		return 1010
	elif row_label == "Cerato":
		return 1011
	elif row_label == "Sportage":
		return 1012
	elif row_label == "Soul":
		return 1013
	elif row_label == "Sportage R":
		return 1014
	elif row_label == "KIA K2 hatchback":
		return 1015
	elif row_label == "Borrego":
		return 1016
	elif row_label == "KIA K5 hybrid":
		return 1017
	elif row_label == "KIA VQ":
		return 1018
	elif row_label == "KIA VQ-R":
		return 1019
	elif row_label == "Shuma":
		return 1020
	elif row_label == "Sorento":
		return 1021
	elif row_label == "New Carens":
		return 1022
	elif row_label == "KIA venga":
		return 1023
	elif row_label == "SPORTAGE":
		return 1024
	elif row_label == "KIA GT":
		return 1025
	elif row_label == "KIA Picanto":
		return 1026
	elif row_label == "KIA Ceed":
		return 1027
	elif row_label == "KIA Trackster":
		return 1028
	elif row_label == "KIA K9":
		return 1029
	elif row_label == "KIA Forte":
		return 1030
	elif row_label == "KIA Provo":
		return 1031
	elif row_label == "KIA CUB":
		return 1032
	elif row_label == "KIA Optima":
		return 1033
	elif row_label == "KIA Cross GT":
		return 1034
	elif row_label == "KIA Ray EV":
		return 1035
	elif row_label == "KIA Niro":
		return 1036
	elif row_label == "GT4 Stinger":
		return 1037
	elif row_label == "Sedona":
		return 1038
	elif row_label == "Kaizun":
		return 1039
	elif row_label == "Roewe 350":
		return 1040
	elif row_label == "Roewe 550 hybrid":
		return 1041
	elif row_label == "Roewe 750":
		return 1042
	elif row_label == "Roewe 750 hybrid":
		return 1043
	elif row_label == "Roewe 950":
		return 1044
	elif row_label == "Roewe E50":
		return 1045
	elif row_label == "Roewe W5":
		return 1046
	elif row_label == "Roewe 550":
		return 1047
	elif row_label == "Outback":
		return 1048
	elif row_label == "Legacy":
		return 1049
	elif row_label == "Legacy estate":
		return 1050
	elif row_label == "Forester":
		return 1051
	elif row_label == "Subaru BRZ":
		return 1052
	elif row_label == "Subaru XV":
		return 1053
	elif row_label == "Impreza hatchback":
		return 1054
	elif row_label == "Impreza sedan":
		return 1055
	elif row_label == "Trezia":
		return 1056
	elif row_label == "Viziv":
		return 1057
	elif row_label == "Subaru WRX":
		return 1058
	elif row_label == "LEVORG":
		return 1059
	elif row_label == "Tribeca":
		return 1060
	elif row_label == "Ciimo":
		return 1061
	elif row_label == "MAXUS G10":
		return 1062
	elif row_label == "MAXUS V80xs":
		return 1063
	elif row_label == "Denza":
		return 1064
	elif row_label == "D-MAX":
		return 1065
	elif row_label == "C2 Cross":
		return 1066
	elif row_label == "c-Elysee sedan":
		return 1067
	elif row_label == "Triomphe":
		return 1068
	elif row_label == "Elysee":
		return 1069
	elif row_label == "Quatre Cross":
		return 1070
	elif row_label == "Quatre hatchback":
		return 1071
	elif row_label == "Quatre sedan":
		return 1072
	elif row_label == "Citroen C2":
		return 1073
	elif row_label == "Citroen C4L":
		return 1074
	elif row_label == "Citroen C5":
		return 1075
	elif row_label == "c-Elysee hatchback":
		return 1076
	elif row_label == "C4 Aircross":
		return 1077
	elif row_label == "Citroen C4":
		return 1078
	elif row_label == "Citroen C3":
		return 1079
	elif row_label == "C3 Picasso":
		return 1080
	elif row_label == "C-Zero":
		return 1081
	elif row_label == "Citroen C-Elysee":
		return 1082
	elif row_label == "Technospace":
		return 1083
	elif row_label == "Lacoste":
		return 1084
	elif row_label == "Metropolis":
		return 1085
	elif row_label == "REVOLTe":
		return 1086
	elif row_label == "Survolt":
		return 1087
	elif row_label == "Tubik":
		return 1088
	elif row_label == "Citroen C-Crosser":
		return 1089
	elif row_label == "Citroen GQ":
		return 1090
	elif row_label == "Citroen GT":
		return 1091
	elif row_label == "Cactus":
		return 1092
	elif row_label == "Citroen C1":
		return 1093
	elif row_label == "B14":
		return 1094
	elif row_label == "Grand C4 Picasso":
		return 1095
	elif row_label == "Power Daily":
		return 1096
	elif row_label == "Duling":
		return 1097
	elif row_label == "Turbo Daily":
		return 1098
	elif row_label == "Campagnola":
		return 1099
	elif row_label == "Massif":
		return 1100
	elif row_label == "Xenia":
		return 1101
	elif row_label == "Copen":
		return 1102
	elif row_label == "Mira":
		return 1103
	elif row_label == "PICO":
		return 1104
	elif row_label == "Kopen":
		return 1105
	elif row_label == "MATERIA":
		return 1106
	elif row_label == "Scion tC":
		return 1107
	elif row_label == "Scion iQ":
		return 1108
	elif row_label == "Scion xB":
		return 1109
	elif row_label == "Scion xA":
		return 1110
	elif row_label == "Scion xD":
		return 1111
	elif row_label == "Scion FR-S":
		return 1112
	elif row_label == "BAC Mono":
		return 1113
	elif row_label == "Vulcano":
		return 1114
	elif row_label == "Tramontana":
		return 1115
	elif row_label == "Lieying":
		return 1116
	elif row_label == "Yongyuanwuxing":
		return 1117
	elif row_label == "Yongyuan A380":
		return 1118
	elif row_label == "Zonda":
		return 1119
	elif row_label == "Huayra":
		return 1120
	elif row_label == "HORKI-1":
		return 1121
	elif row_label == "La Joya":
		return 1122
	elif row_label == "X-BOW":
		return 1123
	elif row_label == "Sagaris":
		return 1124
	elif row_label == "Tuscan":
		return 1125
	elif row_label == "Toyota RAV4":
		return 1126
	elif row_label == "Crown":
		return 1127
	elif row_label == "Corolla":
		return 1128
	elif row_label == "Coaster":
		return 1129
	elif row_label == "Lcruiser":
		return 1130
	elif row_label == "Prado":
		return 1131
	elif row_label == "Prius":
		return 1132
	elif row_label == "Reiz":
		return 1133
	elif row_label == "Vios":
		return 1134
	elif row_label == "Huaguan":
		return 1135
	elif row_label == "FJ Cruiser":
		return 1136
	elif row_label == "Venza":
		return 1137
	elif row_label == "Alphard":
		return 1138
	elif row_label == "Toyota 4 Rinner":
		return 1139
	elif row_label == "Toyota 86":
		return 1140
	elif row_label == "Sequoia":
		return 1141
	elif row_label == "Zelas":
		return 1142
	elif row_label == "Coaster abroad version":
		return 1143
	elif row_label == "Previa":
		return 1144
	elif row_label == "Saina":
		return 1145
	elif row_label == "Toyota IQ":
		return 1146
	elif row_label == "Toyota Aygo":
		return 1147
	elif row_label == "Avensis":
		return 1148
	elif row_label == "Toyota Verso":
		return 1149
	elif row_label == "Toyota MR2":
		return 1150
	elif row_label == "Toyota FT-HS":
		return 1151
	elif row_label == "Undra":
		return 1152
	elif row_label == "Toyota Auris":
		return 1153
	elif row_label == "WISH":
		return 1154
	elif row_label == "Toyota FT-86":
		return 1155
	elif row_label == "Highlander abroad version":
		return 1156
	elif row_label == "Toyota Fun-Vii":
		return 1157
	elif row_label == "Toyota Hilux":
		return 1158
	elif row_label == "Toyota i-Road":
		return 1159
	elif row_label == "Toyota Tacoma":
		return 1160
	elif row_label == "Toyota FCV-R":
		return 1161
	elif row_label == "Toyota FT-CH":
		return 1162
	elif row_label == "Toyota Hi-CT":
		return 1163
	elif row_label == "Toyota NS4":
		return 1164
	elif row_label == "??Avalon":
		return 1165
	elif row_label == "Toyota FT-1":
		return 1166
	elif row_label == "Toyota Matrix":
		return 1167
	elif row_label == "Toyota Urban Cruiser":
		return 1168
	elif row_label == "Toyota 1X":
		return 1169
	elif row_label == "Toyota FT-Bh":
		return 1170
	elif row_label == "Toyota FT-EV":
		return 1171
	elif row_label == "Toyota ME.WE":
		return 1172
	elif row_label == "Toyota RiN":
		return 1173
	elif row_label == "Yuejia":
		return 1174
	elif row_label == "Toyota FCV":
		return 1175
	elif row_label == "YARiS L":
		return 1176
	elif row_label == "Camry":
		return 1177
	elif row_label == "Camry hybrid":
		return 1178
	elif row_label == "Levin":
		return 1179
	elif row_label == "Yaris":
		return 1180
	elif row_label == "EZ":
		return 1181
	elif row_label == "EZ Crossover":
		return 1182
	elif row_label == "Highlander":
		return 1183
	elif row_label == "Fengjing":
		return 1184
	elif row_label == "Fengjing G7":
		return 1185
	elif row_label == "Fengjing Kuaiyun":
		return 1186
	elif row_label == "Mengpaike E":
		return 1187
	elif row_label == "Mengpaike S":
		return 1188
	elif row_label == "Midi":
		return 1189
	elif row_label == "Fukuda":
		return 1190
	elif row_label == "Tunland":
		return 1191
	elif row_label == "Tansuozhe":
		return 1192
	elif row_label == "Tansuozhe III":
		return 1193
	elif row_label == "Xiaochaoren":
		return 1194
	elif row_label == "Xiongshi":
		return 1195
	elif row_label == "Xiongshi F16":
		return 1196
	elif row_label == "Tansuozhe II":
		return 1197
	elif row_label == "Qoros 3":
		return 1198
	elif row_label == "Quros 9":
		return 1199
	elif row_label == "Quros 3 hatchback":
		return 1200
	elif row_label == "E Mei":
		return 1201
	elif row_label == "GX6":
		return 1202
	elif row_label == "Saboo G3":
		return 1203
	elif row_label == "Saboo G5":
		return 1204
	elif row_label == "Saboo GX5":
		return 1205
	elif row_label == "Caiyun 100":
		return 1206
	elif row_label == "Caiyun 300":
		return 1207
	elif row_label == "Caiyun 500":
		return 1208
	elif row_label == "Shuaibao":
		return 1209
	elif row_label == "Shuaijian":
		return 1210
	elif row_label == "Xinglang":
		return 1211
	elif row_label == "Xingwang":
		return 1212
	elif row_label == "Xingwang CL":
		return 1213
	elif row_label == "Xingwang L":
		return 1214
	elif row_label == "Xingwang M1":
		return 1215
	elif row_label == "GP150":
		return 1216
	elif row_label == "Galue":
		return 1217
	elif row_label == "Orochi":
		return 1218
	elif row_label == "Himiko":
		return 1219
	elif row_label == "Fumeilai":
		return 1220
	elif row_label == "Fumeilai VS":
		return 1221
	elif row_label == "Haifuxing":
		return 1222
	elif row_label == "Haima 3":
		return 1223
	elif row_label == "Haima M3":
		return 1224
	elif row_label == "Haima M8":
		return 1225
	elif row_label == "Haima S5":
		return 1226
	elif row_label == "Haima S7":
		return 1227
	elif row_label == "Haimaqishi":
		return 1228
	elif row_label == "Haydo":
		return 1229
	elif row_label == "Premacy":
		return 1230
	elif row_label == "Qiubite":
		return 1231
	elif row_label == "Haima M6":
		return 1232
	elif row_label == "Family M5":
		return 1233
	elif row_label == "Baolige":
		return 1234
	elif row_label == "Lusheng E70":
		return 1235
	elif row_label == "Shengdafei":
		return 1236
	elif row_label == "Tekala":
		return 1237
	elif row_label == "Xinshengdafei":
		return 1238
	elif row_label == "Huatai B11":
		return 1239
	elif row_label == "Hong Qi H7":
		return 1240
	elif row_label == "Hong Qi L5":
		return 1241
	elif row_label == "Hong Qi SUV":
		return 1242
	elif row_label == "Haijing":
		return 1243
	elif row_label == "Haiyue":
		return 1244
	elif row_label == "Yisitanna":
		return 1245
	elif row_label == "Geely GC7":
		return 1246
	elif row_label == "Geely GX2":
		return 1247
	elif row_label == "Geely GX7":
		return 1248
	elif row_label == "Geely SC3":
		return 1249
	elif row_label == "Geely SC5-RV":
		return 1250
	elif row_label == "Geely SC6":
		return 1251
	elif row_label == "Geely SC7":
		return 1252
	elif row_label == "Geely SX7":
		return 1253
	elif row_label == "Geely TX4":
		return 1254
	elif row_label == "King Kong CROSS":
		return 1255
	elif row_label == "King Kong hatchback":
		return 1256
	elif row_label == "King Kong sedan":
		return 1257
	elif row_label == "Jinying":
		return 1258
	elif row_label == "Jinying CROSS":
		return 1259
	elif row_label == "Classic Imperial hatchback":
		return 1260
	elif row_label == "Classic Imperial sedan":
		return 1261
	elif row_label == "Imperial hatchback":
		return 1262
	elif row_label == "Imperial sedan":
		return 1263
	elif row_label == "Panda":
		return 1264
	elif row_label == "Panda CROSS":
		return 1265
	elif row_label == "Vision":
		return 1266
	elif row_label == "Chinese Dragon":
		return 1267
	elif row_label == "Ziyoujian":
		return 1268
	elif row_label == "Geely EV8":
		return 1269
	elif row_label == "Geely EX9":
		return 1270
	elif row_label == "Geely GT":
		return 1271
	elif row_label == "Geely GE":
		return 1272
	elif row_label == "Geely EK-2":
		return 1273
	elif row_label == "Geely IG":
		return 1274
	elif row_label == "Geely EC6-RV":
		return 1275
	elif row_label == "Geely SC7-RV":
		return 1276
	elif row_label == "Geely KC":
		return 1277
	elif row_label == "Geely GX6":
		return 1278
	elif row_label == "Geely GC9":
		return 1279
	elif row_label == "Geely Cross":
		return 1280
	elif row_label == "Geely EC8":
		return 1281
	elif row_label == "Geely GX5":
		return 1282
	elif row_label == "Geely EV7":
		return 1283
	elif row_label == "Geely GS":
		return 1284
	elif row_label == "Geely SX6":
		return 1285
	elif row_label == "Binyue":
		return 1286
	elif row_label == "Heyue A30":
		return 1287
	elif row_label == "Heyue RS":
		return 1288
	elif row_label == "Heyue iEV":
		return 1289
	elif row_label == "Ruifeng":
		return 1290
	elif row_label == "Ruifeng M3":
		return 1291
	elif row_label == "Ruifeng M5":
		return 1292
	elif row_label == "Ruifeng S3":
		return 1293
	elif row_label == "Ruifeng S5":
		return 1294
	elif row_label == "Ruiling":
		return 1295
	elif row_label == "Ruiying":
		return 1296
	elif row_label == "Tongyue":
		return 1297
	elif row_label == "Tongyue Cross":
		return 1298
	elif row_label == "Tongyue RS":
		return 1299
	elif row_label == "Xingrui":
		return 1300
	elif row_label == "Yueyue":
		return 1301
	elif row_label == "Yueyue CROSS":
		return 1302
	elif row_label == "Heyue SC":
		return 1303
	elif row_label == "Heyue A20":
		return 1304
	elif row_label == "Ruifeng M6":
		return 1305
	elif row_label == "Vision IV":
		return 1306
	elif row_label == "Ruifeng A6":
		return 1307
	elif row_label == "Heyue":
		return 1308
	elif row_label == "Baodian":
		return 1309
	elif row_label == "Kairui":
		return 1310
	elif row_label == "Kaiwei":
		return 1311
	elif row_label == "New Yusheng S350":
		return 1312
	elif row_label == "Yuhu":
		return 1313
	elif row_label == "Yuesheng S350":
		return 1314
	elif row_label == "Jinlvhaishi":
		return 1315
	elif row_label == "Dahaishi":
		return 1316
	elif row_label == "Geruisi":
		return 1317
	elif row_label == "Haishi":
		return 1318
	elif row_label == "Haixing":
		return 1319
	elif row_label == "Jinbei S50":
		return 1320
	elif row_label == "Jindian":
		return 1321
	elif row_label == "Leilong":
		return 1322
	elif row_label == "New Haishi":
		return 1323
	elif row_label == "Zhishang S30":
		return 1324
	elif row_label == "Dalishen":
		return 1325
	elif row_label == "Lexus CT":
		return 1326
	elif row_label == "Lexus ES hybrid":
		return 1327
	elif row_label == "Lexus GS":
		return 1328
	elif row_label == "Lexus GS hybrid":
		return 1329
	elif row_label == "Lexus GX":
		return 1330
	elif row_label == "Lexus IS":
		return 1331
	elif row_label == "Lexus IS convertible":
		return 1332
	elif row_label == "Lexus LF-A":
		return 1333
	elif row_label == "Lexus LS":
		return 1334
	elif row_label == "Lexus LS hybrid":
		return 1335
	elif row_label == "Lexus LX":
		return 1336
	elif row_label == "Lexus RC":
		return 1337
	elif row_label == "Lexus RX":
		return 1338
	elif row_label == "Lexus RX hybrid":
		return 1339
	elif row_label == "Lexus LF-Xh":
		return 1340
	elif row_label == "Lexus HS":
		return 1341
	elif row_label == "Lexus LF-LC":
		return 1342
	elif row_label == "Lexus LF-CC":
		return 1343
	elif row_label == "Lexus LF-Gh":
		return 1344
	elif row_label == "Lexus LF-NX":
		return 1345
	elif row_label == "Lexus NX":
		return 1346
	elif row_label == "Lexus ES":
		return 1347
	elif row_label == "Fengshun":
		return 1348
	elif row_label == "Lifan 330":
		return 1349
	elif row_label == "Lifan 520":
		return 1350
	elif row_label == "Lifan 521i":
		return 1351
	elif row_label == "Lifan 530":
		return 1352
	elif row_label == "Lifan 620":
		return 1353
	elif row_label == "Lifan 630":
		return 1354
	elif row_label == "Lifan 720":
		return 1355
	elif row_label == "Lifan X50":
		return 1356
	elif row_label == "Lifan X60":
		return 1357
	elif row_label == "Xingshun":
		return 1358
	elif row_label == "Lifan 320":
		return 1359
	elif row_label == "Jingyue":
		return 1360
	elif row_label == "Lotus L3 hatchback":
		return 1361
	elif row_label == "Lotus L5":
		return 1362
	elif row_label == "Lotus L3 sedan":
		return 1363
	elif row_label == "Ghost":
		return 1364
	elif row_label == "Wraith":
		return 1365
	elif row_label == "Phantom":
		return 1366
	elif row_label == "Atenza":
		return 1367
	elif row_label == "Mazda 8":
		return 1368
	elif row_label == "Mazda CX7":
		return 1369
	elif row_label == "Ruiyi":
		return 1370
	elif row_label == "Ruiyi coupe":
		return 1371
	elif row_label == "Mazda 6":
		return 1372
	elif row_label == "ATENZA":
		return 1373
	elif row_label == "Mazda CX-9":
		return 1374
	elif row_label == "Mazda MX-5":
		return 1375
	elif row_label == "Mazda 3 abroad version":
		return 1376
	elif row_label == "Mazda RX-8":
		return 1377
	elif row_label == "Takeri":
		return 1378
	elif row_label == "Mazda 7 Wagon":
		return 1379
	elif row_label == "Shinari":
		return 1380
	elif row_label == "Hazumi":
		return 1381
	elif row_label == "Mazda 5":
		return 1382
	elif row_label == "Axela hatchback":
		return 1383
	elif row_label == "Mazda 2":
		return 1384
	elif row_label == "Mazda 2 sedan":
		return 1385
	elif row_label == "Mazda 3":
		return 1386
	elif row_label == "Mazda 3 Xingcheng hatchback":
		return 1387
	elif row_label == "Mazda 3 Xingcheng sedan":
		return 1388
	elif row_label == "Mazda CX-5":
		return 1389
	elif row_label == "Axela sedan":
		return 1390
	elif row_label == "Maybach":
		return 1391
	elif row_label == "Acura ILX":
		return 1392
	elif row_label == "Acura MDX":
		return 1393
	elif row_label == "Acura RDX":
		return 1394
	elif row_label == "Acura RL":
		return 1395
	elif row_label == "Acura RLX":
		return 1396
	elif row_label == "Acura TL":
		return 1397
	elif row_label == "Acura ZDX":
		return 1398
	elif row_label == "Acura NSX":
		return 1399
	elif row_label == "Acura SUV-X":
		return 1400
	elif row_label == "Acura TLX":
		return 1401
	elif row_label == "Acura ILX hybrid":
		return 1402
	elif row_label == "Eastar":
		return 1403
	elif row_label == "Eastar Cross":
		return 1404
	elif row_label == "Fulwin 2 hatchback":
		return 1405
	elif row_label == "Fulwin 2 sedan":
		return 1406
	elif row_label == "Chrey A1":
		return 1407
	elif row_label == "Chrey A3 hatchback":
		return 1408
	elif row_label == "Chrey A3 sedan":
		return 1409
	elif row_label == "Chrey A5":
		return 1410
	elif row_label == "Chrey E3":
		return 1411
	elif row_label == "Chrey E5":
		return 1412
	elif row_label == "Chrey QQ":
		return 1413
	elif row_label == "Chrey QQ3":
		return 1414
	elif row_label == "Chrey QQme":
		return 1415
	elif row_label == "Chrey X1":
		return 1416
	elif row_label == "Chrey Aika":
		return 1417
	elif row_label == "Cowin 1":
		return 1418
	elif row_label == "Cowin 2":
		return 1419
	elif row_label == "Cowin 3":
		return 1420
	elif row_label == "Cowin 5":
		return 1421
	elif row_label == "Tiggo":
		return 1422
	elif row_label == "Tiggo 3":
		return 1423
	elif row_label == "Tiggo 5":
		return 1424
	elif row_label == "Chrey M14":
		return 1425
	elif row_label == "Chrey @ANT":
		return 1426
	elif row_label == "Chrey TX":
		return 1427
	elif row_label == "Arrizo 7":
		return 1428
	elif row_label == "Riich G3":
		return 1429
	elif row_label == "Riich G6":
		return 1430
	elif row_label == "Riich M1":
		return 1431
	elif row_label == "Riich M5":
		return 1432
	elif row_label == "Ruiqi G5":
		return 1433
	elif row_label == "smart fortwo":
		return 1434
	elif row_label == "smart for-us":
		return 1435
	elif row_label == "smart forjeremy":
		return 1436
	elif row_label == "smart forstars":
		return 1437
	elif row_label == "smart forfour":
		return 1438
	elif row_label == "smart fortwo electric":
		return 1439
	elif row_label == "Shuanghuan SCEO":
		return 1440
	elif row_label == "Nobel":
		return 1441
	elif row_label == "Fujia":
		return 1442
	elif row_label == "Volvo C30":
		return 1443
	elif row_label == "Volvo S60":
		return 1444
	elif row_label == "Volvo V40":
		return 1445
	elif row_label == "Volvo V40 CrossCountry":
		return 1446
	elif row_label == "Volvo V60":
		return 1447
	elif row_label == "Volvo XC60":
		return 1448
	elif row_label == "Volvo XC90 abroad version":
		return 1449
	elif row_label == "Volvo S80":
		return 1450
	elif row_label == "Volvo V50":
		return 1451
	elif row_label == "Volvo V70":
		return 1452
	elif row_label == "Volvo XC70":
		return 1453
	elif row_label == "Universe":
		return 1454
	elif row_label == "Volvo You":
		return 1455
	elif row_label == "Air Motion":
		return 1456
	elif row_label == "Volvo Coupe":
		return 1457
	elif row_label == "Volvo XC Coupe":
		return 1458
	elif row_label == "ESTATE":
		return 1459
	elif row_label == "Volvo C70":
		return 1460
	elif row_label == "Volvo S40":
		return 1461
	elif row_label == "Volvo S80L":
		return 1462
	elif row_label == "Volvo S60L":
		return 1463
	elif row_label == "Volvo XC Classic":
		return 1464
	elif row_label == "Volvo S60L hybrid":
		return 1465
	elif row_label == "Wiesmann Roadster":
		return 1466
	elif row_label == "Wiesmann Spyder":
		return 1467
	elif row_label == "Wiesmann GT":
		return 1468
	elif row_label == "Alhambra":
		return 1469
	elif row_label == "Seat IBL":
		return 1470
	elif row_label == "Seat LEON":
		return 1471
	elif row_label == "Ibiza":
		return 1472
	elif row_label == "Ibiza estate":
		return 1473
	elif row_label == "Seat ALTEA":
		return 1474
	elif row_label == "Seat EXEO":
		return 1475
	elif row_label == "Seat IBX":
		return 1476
	elif row_label == "Seat Mii":
		return 1477
	elif row_label == "Seat IBE":
		return 1478
	elif row_label == "Mustang F16":
		return 1479
	elif row_label == "Mustang F99":
		return 1480
	elif row_label == "Mustang A-MPV":
		return 1481
	elif row_label == "Mustang T70":
		return 1482
	elif row_label == "Mustang M31D":
		return 1483
	elif row_label == "Mustang M302":
		return 1484
	elif row_label == "Mustang F12":
		return 1485
	elif row_label == "MiTo":
		return 1486
	elif row_label == "159":
		return 1487
	elif row_label == "Giulietta":
		return 1488
	elif row_label == "4C":
		return 1489
	elif row_label == "2uettottanta":
		return 1490
	elif row_label == "TZ3":
		return 1491
	elif row_label == "Disco Volante":
		return 1492
	elif row_label == "Gloria":
		return 1493
	elif row_label == "8C":
		return 1494
	elif row_label == "Zenvo ST1":
		return 1495
	elif row_label == "Knight XV":
		return 1496
	elif row_label == " Hector":
		return 1497
	elif row_label == "Enranger G3":
		return 1498
	elif row_label == "AC Schnitzer 1 Class":
		return 1499
	elif row_label == "AC Schnitzer 5 Class":
		return 1500
	elif row_label == "AC Schnitzer 6 Class":
		return 1501
	elif row_label == "AC Schnitzer 7 Class":
		return 1502
	elif row_label == "AC Schnitzer MINI":
		return 1503
	elif row_label == "AC Schnitzer X1":
		return 1504
	elif row_label == "AC Schnitzer X3":
		return 1505
	elif row_label == "AC Schnitzer X5":
		return 1506
	elif row_label == "AC Schnitzer X6":
		return 1507
	elif row_label == "AC Schnitzer 3 Class":
		return 1508
	elif row_label == "Atlantic":
		return 1509
	elif row_label == "Surf":
		return 1510
	elif row_label == "Latigo":
		return 1511
	elif row_label == "Tramonto":
		return 1512
	elif row_label == "Karma":
		return 1513
	elif row_label == "Lancia Flavia":
		return 1514
	elif row_label == "Lancia Thema":
		return 1515
	elif row_label == "Lancia Voyager":
		return 1516
	elif row_label == "Lancia Ypsilon":
		return 1517
	elif row_label == "Lancia Delta":
		return 1518
	elif row_label == "Lancia Stratos":
		return 1519
	elif row_label == "Youjin":
		return 1520
	elif row_label == "Youya":
		return 1521
	elif row_label == "Youyou":
		return 1522
	elif row_label == "Youpai":
		return 1523
	elif row_label == "Yousheng":
		return 1524
	elif row_label == "Alto":
		return 1525
	elif row_label == "Cultus":
		return 1526
	elif row_label == "Alivio":
		return 1527
	elif row_label == "Tianyu SX4 hatchback":
		return 1528
	elif row_label == "Tianyu SX4 sedan":
		return 1529
	elif row_label == "Tianyushangyue":
		return 1530
	elif row_label == "Yuyan":
		return 1531
	elif row_label == "Fengyu":
		return 1532
	elif row_label == "Grand Vitara":
		return 1533
	elif row_label == "Kazishi":
		return 1534
	elif row_label == "Swift":
		return 1535
	elif row_label == "S-CROSS abroad version":
		return 1536
	elif row_label == "SX4 S-CROSS":
		return 1537
	elif row_label == "Regina":
		return 1538
	elif row_label == "Authentics":
		return 1539
	elif row_label == "Suzuki iV-4":
		return 1540
	elif row_label == "Crosshiker":
		return 1541
	elif row_label == "X-Lander":
		return 1542
	elif row_label == "Jimny":
		return 1543
	elif row_label == "Bei Douxing":
		return 1544
	elif row_label == "Liana A6 hatchback":
		return 1545
	elif row_label == "Liana A6 sedan":
		return 1546
	elif row_label == "Liana hatchback":
		return 1547
	elif row_label == "Liana sedan":
		return 1548
	elif row_label == "Splash":
		return 1549
	elif row_label == "Landy":
		return 1550
	elif row_label == "Linian S1":
		return 1551
	elif row_label == "Elise":
		return 1552
	elif row_label == "Exige":
		return 1553
	elif row_label == "Elan":
		return 1554
	elif row_label == "Elite":
		return 1555
	elif row_label == "Eterne":
		return 1556
	elif row_label == "Evora":
		return 1557
	elif row_label == "MG3 SW":
		return 1558
	elif row_label == "MG3 Xross":
		return 1559
	elif row_label == "MG5":
		return 1560
	elif row_label == "MG6 sedan":
		return 1561
	elif row_label == "MG6 hatchback":
		return 1562
	elif row_label == "MG7":
		return 1563
	elif row_label == "Icon":
		return 1564
	elif row_label == "MG CS":
		return 1565
	elif row_label == "MG3":
		return 1566
	elif row_label == "McLaren 12C":
		return 1567
	elif row_label == "McLaren P1":
		return 1568
	elif row_label == "McLaren X-1":
		return 1569
	elif row_label == "McLaren 650S":
		return 1570
	elif row_label == "Antara":
		return 1571
	elif row_label == "Zafira":
		return 1572
	elif row_label == "GTC convertible":
		return 1573
	elif row_label == "GTC hatchback":
		return 1574
	elif row_label == "GTC sedan":
		return 1575
	elif row_label == "Insignia":
		return 1576
	elif row_label == "Opel AMPERA":
		return 1577
	elif row_label == "Opel CORSA":
		return 1578
	elif row_label == "Opel Adam":
		return 1579
	elif row_label == "Opel Cascada":
		return 1580
	elif row_label == "Opel Combo":
		return 1581
	elif row_label == "Opel Mokka":
		return 1582
	elif row_label == "Opel Monza":
		return 1583
	elif row_label == "Meriva":
		return 1584
	elif row_label == "Chenfeng":
		return 1585
	elif row_label == "Venucia R30":
		return 1586
	elif row_label == "Venucia R50":
		return 1587
	elif row_label == "Venucia R50X":
		return 1588
	elif row_label == "Venucia ViWa":
		return 1589
	elif row_label == "Venucia D50":
		return 1590
	elif row_label == "ASX":
		return 1591
	elif row_label == "Pajero Sport":
		return 1592
	elif row_label == "Pajero":
		return 1593
	elif row_label == "Grandis":
		return 1594
	elif row_label == "Eclipse":
		return 1595
	elif row_label == "Evo":
		return 1596
	elif row_label == "Mitsubishi i":
		return 1597
	elif row_label == "Mitsubishi Colt":
		return 1598
	elif row_label == "ASX abroad version":
		return 1599
	elif row_label == "Global Small":
		return 1600
	elif row_label == "Mirage":
		return 1601
	elif row_label == "Mitsubishi G4":
		return 1602
	elif row_label == "Endeavor":
		return 1603
	elif row_label == "Mitsubishi CA-MiEV":
		return 1604
	elif row_label == "Mitsubishi GR-HEV":
		return 1605
	elif row_label == "Mitsubishi PX-MiEV":
		return 1606
	elif row_label == "Mitsubishi XR-PHEV":
		return 1607
	elif row_label == "eK Space":
		return 1608
	elif row_label == "Outlander abroad version":
		return 1609
	elif row_label == "Mitsubishi Fortis":
		return 1610
	elif row_label == "Mitsubishi Zinger":
		return 1611
	elif row_label == "Mitsubishi Lancer":
		return 1612
	elif row_label == "Mitsubishi Lancer EX":
		return 1613
	elif row_label == "Mitsubishi Galant":
		return 1614
	elif row_label == "SAAB D50":
		return 1615
	elif row_label == "SAAB D70":
		return 1616
	elif row_label == "SAAB D60":
		return 1617
	elif row_label == "Spyker C8":
		return 1618
	elif row_label == "Spyker C12":
		return 1619
	elif row_label == "Spyker B6":
		return 1620
	elif row_label == "Spirra":
		return 1621
	elif row_label == "Wulinghongguang":
		return 1622
	elif row_label == "Wulingzhiguang":
		return 1623
	elif row_label == "Xingwang":
		return 1624
	elif row_label == "Xiaoxuanfeng":
		return 1625
	elif row_label == "Wulingrongguang":
		return 1626
	elif row_label == "AVEO hatchback":
		return 1627
	elif row_label == "Trax":
		return 1628
	elif row_label == "Epica":
		return 1629
	elif row_label == "Cruze sedan":
		return 1630
	elif row_label == "Cruze hatchback":
		return 1631
	elif row_label == "Captiva":
		return 1632
	elif row_label == "Aveo":
		return 1633
	elif row_label == "Lova":
		return 1634
	elif row_label == "Malibu":
		return 1635
	elif row_label == "Sail hatchback":
		return 1636
	elif row_label == "Sail sedan":
		return 1637
	elif row_label == "Sail SPRINGO":
		return 1638
	elif row_label == "Aveo sedan":
		return 1639
	elif row_label == "Volt":
		return 1640
	elif row_label == "Spark":
		return 1641
	elif row_label == "CHEVY Traverse":
		return 1642
	elif row_label == "CHEVY Beat":
		return 1643
	elif row_label == "CHEVY Orlando":
		return 1644
	elif row_label == "Sonic":
		return 1645
	elif row_label == "Cruze abroad version":
		return 1646
	elif row_label == "CHEVY Trax":
		return 1647
	elif row_label == "Corvette":
		return 1648
	elif row_label == "Silverado":
		return 1649
	elif row_label == "CHEVY SS":
		return 1650
	elif row_label == "Agile":
		return 1651
	elif row_label == "Caprice":
		return 1652
	elif row_label == "Colorado":
		return 1653
	elif row_label == "Equinox":
		return 1654
	elif row_label == "Impala":
		return 1655
	elif row_label == "TrailBlazer":
		return 1656
	elif row_label == "Cobalt":
		return 1657
	elif row_label == "CHEVY Code":
		return 1658
	elif row_label == "CHEVY Miray":
		return 1659
	elif row_label == "CHEVY Onix":
		return 1660
	elif row_label == "CHEVY Tahoe":
		return 1661
	elif row_label == "CHEVY Tru":
		return 1662
	elif row_label == "Express":
		return 1663
	elif row_label == "Suburban":
		return 1664
	elif row_label == "City Express":
		return 1665
	elif row_label == "Camaro":
		return 1666
	elif row_label == "Kaisheng 2":
		return 1667
	elif row_label == "Zhonghua H220":
		return 1668
	elif row_label == "Zhonghua H320":
		return 1669
	elif row_label == "Zhonghua H330":
		return 1670
	elif row_label == "Zhonghua H530":
		return 1671
	elif row_label == "Zhonghua V5":
		return 1672
	elif row_label == "Zhonghua Junjie":
		return 1673
	elif row_label == "Zhonghua Junjie CROSS":
		return 1674
	elif row_label == "Zhonghua Junjie FRV":
		return 1675
	elif row_label == "Zhonghua Junjie FSV":
		return 1676
	elif row_label == "Zhonghua Junjie Wagon":
		return 1677
	elif row_label == "Zhonghua Zunchi":
		return 1678
	elif row_label == "Zhonghua H230":
		return 1679
	elif row_label == "Brabus S Class":
		return 1680
	elif row_label == "Brabus GL Class":
		return 1681
	elif row_label == "Brabus M Class":
		return 1682
	elif row_label == "Brabus smart fortwo":
		return 1683
	elif row_label == "Brabus CLS Class":
		return 1684
	elif row_label == "Brabus A Class":
		return 1685
	elif row_label == "Brabus B Class":
		return 1686
	elif row_label == "Brabus CL Class":
		return 1687
	elif row_label == "Brabus G Class":
		return 1688
	elif row_label == "Brabus SLK Class":
		return 1689
	elif row_label == "Brabus SLS Class":
		return 1690
	elif row_label == "Brabus SL Class":
		return 1691
	elif row_label == "Brabus E Class":
		return 1692
	elif row_label == "Evantra":
		return 1693
	elif row_label == "MELKUS RS2000":
		return 1694
	elif row_label == "Changling":
		return 1695
	elif row_label == "Grandtiger F1":
		return 1696
	elif row_label == "Grandtiger G3":
		return 1697
	elif row_label == "Grandtiger TUV":
		return 1698
	elif row_label == "Grandtiger abroad version":
		return 1699
	elif row_label == "Quick":
		return 1700
	elif row_label == "Quick V5":
		return 1701
	elif row_label == "Quick V7":
		return 1702
	elif row_label == "Zxauto C3":
		return 1703
	elif row_label == "GreenWheel":
		return 1704
	elif row_label == "Grandtiger SUV":
		return 1705
	elif row_label == "Qijian A9":
		return 1706
	elif row_label == "Carlsson C":
		return 1707
	elif row_label == "CarlssonCS":
		return 1708
	elif row_label == "CarlssonCK":
		return 1709
	elif row_label == "CarlssonCML":
		return 1710
	elif row_label == "CarlssonCGL":
		return 1711
	elif row_label == "Shouwang":
		return 1712
	elif row_label == "Noble M600":
		return 1713
	elif row_label == "Noble M14":
		return 1714
	elif row_label == "Noble M15":
		return 1715
	elif row_label == "Noble M12":
		return 1716
	else:
		return 0


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    basename = group.filename
    fullname = basename + ".jpg"
    #print(path)
    #print(os.path.join(path, '{}'.format(fullname))
    #print(fullname)
    #print (group._fields)
    #group._replace(filename=fullname)
    #print(group.filename)
    #print(group)
    with tf.gfile.GFile(os.path.join(path, '{}'.format(fullname)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    fullname = fullname.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(str(row['class']).encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(fullname),
        'image/source_id': dataset_util.bytes_feature(fullname),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(FLAGS.image_dir)
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()
