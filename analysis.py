from utils import profile


def bigram(text):
    import misc
    uppertext = text.upper()
    filteredtext = misc.filter(uppertext)
    frequencies = {}

    for index in range(len(filteredtext) - 1):
        bigram = filteredtext[index:index + 2]
        if bigram in frequencies:
            frequencies[bigram] += 1
        else:
            frequencies[bigram] = 1

    return frequencies


def pmcc_b(text):
    import math
    import misc
    alphabet = ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ',
                'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ',
                'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR',
                'BS', 'BT', 'BU', 'BV', 'BW', 'BY',
                'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ',
                'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY',
                'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ',
                'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DY',
                'EA', 'EB', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ',
                'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF', 'FG', 'FH', 'FI', 'FJ', 'FK', 'FL', 'FM', 'FN', 'FO', 'FP', 'FQ',
                'FR', 'FS', 'FT', 'FU', 'FV', 'FW', 'FY',
                'GA', 'GB', 'GC', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GJ', 'GK', 'GL', 'GM', 'GN', 'GO', 'GP', 'GQ',
                'GR', 'GS', 'GT', 'GU', 'GV', 'GW', 'GX', 'GY', 'GZ',
                'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HJ', 'HK', 'HL', 'HM', 'HN', 'HO', 'HP', 'HQ',
                'HR', 'HS', 'HT', 'HU', 'HV', 'HW', 'HY',
                'IA', 'IB', 'IC', 'ID', 'IE', 'IF', 'IG', 'IH', 'II', 'IJ', 'IK', 'IL', 'IM', 'IN', 'IO', 'IP', 'IQ',
                'IR', 'IS', 'IT', 'IU', 'IV', 'IW', 'IX', 'IY', 'IZ',
                'JA', 'JE', 'JI', 'JO', 'JU',
                'KA', 'KB', 'KC', 'KD', 'KE', 'KF', 'KG', 'KH', 'KI', 'KJ', 'KK', 'KL', 'KM', 'KN', 'KO', 'KP', 'KQ',
                'KR', 'KS', 'KT', 'KU', 'KV', 'KW', 'KY',
                'LA', 'LB', 'LC', 'LD', 'LE', 'LF', 'LG', 'LH', 'LI', 'LJ', 'LK', 'LL', 'LM', 'LN', 'LO', 'LP', 'LR',
                'LS', 'LT', 'LU', 'LV', 'LW', 'LX', 'LY', 'LZ',
                'MA', 'MB', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MI', 'MJ', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ',
                'MR', 'MS', 'MT', 'MU', 'MW', 'MY',
                'NA', 'NB', 'NC', 'ND', 'NE', 'NF', 'NG', 'NH', 'NI', 'NJ', 'NK', 'NL', 'NM', 'NN', 'NO', 'NP', 'NQ',
                'NR', 'NS', 'NT', 'NU', 'NV', 'NW', 'NX', 'NY', 'NZ',
                'OA', 'OB', 'OC', 'OD', 'OE', 'OF', 'OG', 'OH', 'OI', 'OJ', 'OK', 'OL', 'OM', 'ON', 'OO', 'OP', 'OQ',
                'OR', 'OS', 'OT', 'OU', 'OV', 'OW', 'OX', 'OY', 'OZ',
                'PA', 'PB', 'PC', 'PD', 'PE', 'PF', 'PG', 'PH', 'PI', 'PJ', 'PL', 'PM', 'PN', 'PO', 'PP', 'PQ', 'PR',
                'PS', 'PT', 'PU', 'PW', 'PY',
                'QU',
                'RA', 'RB', 'RC', 'RD', 'RE', 'RF', 'RG', 'RH', 'RI', 'RJ', 'RK', 'RL', 'RM', 'RN', 'RO', 'RP', 'RQ',
                'RR', 'RS', 'RT', 'RU', 'RV', 'RW', 'RY',
                'SA', 'SB', 'SC', 'SD', 'SE', 'SF', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SQ',
                'SR', 'SS', 'ST', 'SU', 'SV', 'SW', 'SY',
                'TA', 'TB', 'TC', 'TD', 'TE', 'TF', 'TG', 'TH', 'TI', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TP', 'TQ',
                'TR', 'TS', 'TT', 'TU', 'TV', 'TW', 'TY', 'TZ',
                'UA', 'UB', 'UC', 'UD', 'UE', 'UF', 'UG', 'UH', 'UI', 'UJ', 'UK', 'UL', 'UM', 'UN', 'UO', 'UP', 'UR',
                'US', 'UT', 'UU', 'UV', 'UW', 'UX', 'UY', 'UZ',
                'VA', 'VB', 'VE', 'VI', 'VO', 'VS', 'VT', 'VU', 'VY',
                'WA', 'WB', 'WC', 'WD', 'WE', 'WF', 'WG', 'WH', 'WI', 'WJ', 'WK', 'WL', 'WM', 'WN', 'WO', 'WP', 'WQ',
                'WR', 'WS', 'WT', 'WU', 'WV', 'WW', 'WY',
                'XA', 'XB', 'XC', 'XE', 'XF', 'XH', 'XI', 'XL', 'XM', 'XO', 'XP', 'XT', 'XU', 'XW', 'XY',
                'YA', 'YB', 'YC', 'YD', 'YE', 'YF', 'YG', 'YH', 'YI', 'YJ', 'YK', 'YL', 'YM', 'YN', 'YO', 'YP', 'YQ',
                'YR', 'YS', 'YT', 'YU', 'YV', 'YW', 'YY', 'YZ',
                'ZA', 'ZE', 'ZF', 'ZI', 'ZL', 'ZO', 'ZR', 'ZU', 'ZW', 'ZY', 'ZZ', ]

    ct = text.upper()
    filteredtext = misc.filter(ct)
    fx = bigram(filteredtext)
    fy = {'LO': 1145, 'OR': 1613, 'RD': 445, 'DO': 1122, 'OF': 1773, 'FT': 892, 'TH': 10210, 'HE': 9611, 'EF': 1064,
          'FL': 337, 'LI': 1341, 'IE': 519, 'ES': 3164, 'SA': 1715, 'AN': 4311, 'NO': 1236, 'OV': 334, 'VE': 1244,
          'EL': 1436, 'LB': 95, 'BY': 260, 'YW': 367, 'WI': 857, 'IL': 829, 'LL': 1399, 'IA': 114, 'AM': 761, 'MG': 29,
          'GO': 727, 'OL': 512, 'LD': 632, 'DI': 982, 'IN': 4667, 'NG': 2685, 'GC': 59, 'CO': 963, 'ON': 2600,
          'NT': 3135, 'TE': 1924, 'EN': 2550, 'TS': 795, 'ST': 2889, 'SO': 1127, 'OU': 2707, 'UN': 1248, 'ND': 3781,
          'SH': 1422, 'LF': 222, 'FI': 629, 'IR': 834, 'RE': 3921, 'EO': 812, 'EM': 1157, 'MO': 1006, 'TA': 1343,
          'AI': 1135, 'NH': 394, 'HU': 364, 'UT': 1170, 'EB': 823, 'BE': 1322, 'EA': 3160, 'AC': 1409, 'CH': 1117,
          'HP': 81, 'PA': 652, 'ED': 4174, 'DF': 344, 'FA': 535, 'CE': 929, 'DL': 355, 'GH': 1057, 'HA': 2454,
          'RB': 161, 'AS': 2475, 'TF': 263, 'FR': 511, 'RO': 1711, 'OM': 897, 'MW': 102, 'WA': 2021, 'AT': 2862,
          'ER': 4300, 'MA': 753, 'RS': 772, 'AD': 937, 'OW': 1316, 'WS': 102, 'DT': 1737, 'AL': 2044, 'LT': 446,
          'TR': 820, 'EE': 1361, 'SG': 164, 'GI': 270, 'IF': 340, 'FO': 939, 'RT': 947, 'DA': 1425, 'AR': 1699,
          'RK': 197, 'KN': 282, 'NE': 1482, 'SS': 1194, 'AV': 476, 'VI': 179, 'EW': 1341, 'WT': 178, 'TO': 2635,
          'OA': 271, 'DE': 1214, 'HT': 1032, 'LA': 1162, 'EG': 474, 'GL': 313, 'SE': 1607, 'SC': 517, 'CA': 791,
          'TL': 590, 'LE': 1771, 'OC': 365, 'CK': 1227, 'KC': 58, 'CR': 445, 'RY': 311, 'YO': 898, 'EH': 793, 'SN': 313,
          'OT': 1418, 'SF': 366, 'RM': 273, 'MY': 113, 'YM': 108, 'RA': 1875, 'RC': 211, 'AP': 415, 'PT': 287,
          'ET': 2278, 'BO': 625, 'OY': 260, 'IT': 1625, 'HF': 86, 'RH': 257, 'RL': 146, 'WE': 1343, 'DH': 684,
          'HI': 3017, 'IM': 1097, 'MS': 281, 'FD': 46, 'WN': 396, 'FE': 418, 'WF': 48, 'KA': 248, 'DB': 511, 'GA': 736,
          'OP': 417, 'PI': 802, 'IC': 751, 'KH': 131, 'IS': 2086, 'SW': 657, 'AY': 594, 'YT': 594, 'AG': 579,
          'OO': 1083, 'HO': 1008, 'UG': 450, 'HH': 206, 'AK': 306, 'KE': 1106, 'FF': 270, 'FH': 185, 'LS': 179,
          'TN': 150, 'GR': 492, 'EY': 833, 'YS': 574, 'TU': 376, 'UC': 234, 'KT': 206, 'OH': 245, 'RW': 236, 'SP': 627,
          'PL': 354, 'LR': 90, 'MT': 335, 'GS': 325, 'SM': 374, 'EJ': 94, 'JU': 114, 'AB': 450, 'BA': 364, 'CL': 349,
          'MB': 315, 'RI': 1160, 'LY': 986, 'YA': 486, 'GT': 579, 'EC': 1270, 'EP': 803, 'PE': 911, 'BR': 340,
          'OK': 661, 'RU': 334, 'NK': 253, 'KS': 281, 'WH': 989, 'NA': 768, 'BI': 155, 'SI': 1133, 'IO': 380, 'DY': 231,
          'YE': 285, 'DU': 276, 'UP': 474, 'PW': 45, 'DS': 925, 'AW': 392, 'TC': 283, 'HL': 105, 'IK': 235, 'OE': 85,
          'II': 2, 'ID': 861, 'DW': 448, 'MI': 428, 'NU': 124, 'EU': 156, 'RG': 109, 'TT': 1798, 'MU': 189, 'UL': 730,
          'TI': 1464, 'UD': 194, 'DR': 580, 'PS': 191, 'LP': 868, 'GW': 132, 'EV': 375, 'VO': 137, 'OI': 425,
          'IG': 1243, 'AU': 327, 'PP': 259, 'DJ': 116, 'JE': 35, 'KI': 370, 'CG': 4, 'GE': 697, 'UR': 813, 'TM': 166,
          'MF': 62, 'ME': 1362, 'PO': 406, 'NI': 573, 'HS': 298, 'TW': 744, 'SY': 113, 'DC': 220, 'SK': 144, 'LU': 259,
          'UM': 193, 'MP': 264, 'PC': 17, 'RN': 303, 'NS': 795, 'TD': 161, 'NR': 148, 'FU': 243, 'DV': 47, 'YF': 145,
          'AF': 213, 'OD': 527, 'DG': 205, 'GM': 53, 'NL': 274, 'HR': 291, 'CT': 195, 'NW': 289, 'PH': 899, 'SL': 508,
          'NY': 243, 'YG': 68, 'TB': 309, 'YL': 126, 'TP': 149, 'BU': 466, 'SU': 374, 'NF': 143, 'MM': 75, 'US': 779,
          'YB': 178, 'UA': 119, 'OS': 563, 'IB': 159, 'BL': 585, 'OB': 259, 'DN': 288, 'BV': 7, 'YU': 33, 'YH': 276,
          'RR': 313, 'MN': 81, 'IZ': 70, 'ZE': 92, 'DD': 352, 'NN': 150, 'YN': 66, 'OG': 272, 'HW': 175, 'GD': 57,
          'RP': 128, 'YR': 123, 'JA': 393, 'GG': 526, 'KF': 49, 'TG': 84, 'MD': 23, 'EK': 94, 'EI': 675, 'NB': 169,
          'PR': 277, 'CQ': 1, 'QU': 175, 'NC': 732, 'YC': 129, 'VA': 151, 'GU': 164, 'UE': 183, 'EX': 197, 'XP': 79,
          'TY': 279, 'UH': 46, 'IP': 145, 'DM': 153, 'CC': 68, 'FM': 42, 'HM': 78, 'AA': 26, 'SR': 207, 'IW': 67,
          'YI': 261, 'LW': 98, 'FP': 62, 'IV': 234, 'CS': 41, 'KO': 100, 'HB': 88, 'UB': 116, 'BB': 76, 'MH': 105,
          'DQ': 16, 'UI': 179, 'KL': 103, 'PU': 164, 'MR': 31, 'NJ': 49, 'HD': 54, 'FC': 87, 'LM': 109, 'AH': 87,
          'HC': 72, 'DP': 275, 'SB': 273, 'RF': 147, 'SD': 123, 'KB': 71, 'WY': 32, 'TV': 14, 'CI': 258, 'KU': 31,
          'HG': 33, 'AZ': 36, 'ZZ': 16, 'ZL': 6, 'GB': 111, 'LV': 53, 'WM': 18, 'WK': 3, 'KW': 114, 'OX': 4, 'XE': 11,
          'FS': 169, 'LH': 106, 'TJ': 64, 'HK': 9, 'XC': 42, 'KV': 2, 'ZI': 11, 'XT': 44, 'EZ': 21, 'YD': 105,
          'GY': 443, 'YP': 104, 'AO': 14, 'GP': 70, 'GN': 121, 'SQ': 81, 'KG': 24, 'HY': 102, 'SV': 63, 'NV': 49,
          'AQ': 10, 'LN': 37, 'GF': 92, 'ZO': 28, 'FG': 31, 'NP': 95, 'WB': 22, 'YY': 52, 'KY': 57, 'MC': 48, 'AJ': 17,
          'FW': 94, 'VY': 12, 'LC': 38, 'CU': 172, 'IU': 13, 'WD': 31, 'WW': 59, 'ML': 36, 'WR': 51, 'FB': 81, 'HN': 49,
          'BT': 33, 'WL': 76, 'TK': 55, 'WO': 455, 'LG': 62, 'NM': 60, 'KP': 32, 'LK': 101, 'PF': 21, 'BS': 37, 'BN': 2,
          'FY': 76, 'UW': 55, 'UY': 3, 'SJ': 38, 'BD': 3, 'YV': 15, 'PB': 24, 'UK': 26, 'WU': 19, 'KR': 41, 'IX': 12,
          'XY': 7, 'PM': 13, 'JO': 57, 'FN': 20, 'RJ': 25, 'TQ': 3, 'XI': 9, 'WP': 17, 'WC': 22, 'XA': 16, 'CW': 22,
          'CY': 21, 'MJ': 14, 'MQ': 4, 'KM': 26, 'OJ': 24, 'UZ': 12, 'ZW': 1, 'IH': 28, 'FV': 11, 'HJ': 31, 'UO': 21,
          'UF': 30, 'YJ': 37, 'IJ': 4, 'ZA': 11, 'ZR': 1, 'KJ': 17, 'WG': 8, 'PY': 28, 'RV': 36, 'XH': 5, 'KD': 23,
          'BW': 4, 'DK': 28, 'PN': 7, 'HV': 1, 'EQ': 30, 'AX': 12, 'NZ': 3, 'ZY': 3, 'BH': 5, 'YK': 20, 'WV': 2,
          'GJ': 16, 'RQ': 2, 'FK': 4, 'PJ': 6, 'UV': 10, 'UJ': 8, 'KK': 2, 'FJ': 9, 'MK': 5, 'LJ': 14, 'BM': 4, 'VS': 3,
          'BJ': 10, 'WJ': 8, 'YQ': 8, 'CB': 7, 'OQ': 1, 'XL': 2, 'CD': 2, 'XO': 4, 'GQ': 4, 'JI': 2, 'NX': 5, 'XU': 6,
          'GK': 5, 'ZF': 1, 'PD': 3, 'NQ': 8, 'YZ': 2, 'BG': 1, 'VU': 6, 'OZ': 7, 'UU': 6, 'VT': 1, 'XB': 1, 'CF': 8,
          'PQ': 1, 'GV': 5, 'KQ': 1, 'UX': 1, 'XF': 3, 'CP': 6, 'AE': 2, 'IY': 1, 'CN': 3, 'PG': 3, 'CM': 3, 'HQ': 2,
          'TZ': 2, 'ZU': 2, 'BF': 1, 'XW': 1, 'WQ': 2, 'XM': 1, 'IQ': 1, 'LZ': 3, 'VB': 1}
    sigxy = 0
    sigx = 0
    sigy = 0
    sigxsquared = 0
    sigysquared = 0
    for i in range(len(alphabet)):
        bigramVal = alphabet[i]

        fxVal = 0
        fyVal = 0

        try:
            fxVal = fx[bigramVal]
        except KeyError:
            pass

        try:
            fyVal = fy[bigramVal]
        except KeyError:
            pass

        sigxy += fxVal * fyVal
        sigx += fxVal
        sigy += fyVal
        sigxsquared += fxVal ** 2
        sigysquared += fyVal ** 2

    topright = (sigx * sigy) / 26 ** 2
    top = sigxy - topright
    bottomleft = sigxsquared - ((sigx) ** 2) / 26 ** 2
    bottomright = sigysquared - ((sigy) ** 2) / 26 ** 2
    bottom = math.sqrt(bottomleft * bottomright)
    if bottom == 0:  # Occurs when CT contains no valid bigrams
        return 0

    pmccf = top / bottom
    return pmccf
