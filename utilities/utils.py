import random

import softest

from utilities import ExcelUtil


class Utils(softest.TestCase):
    def assertListItemText(self,list,value):
        for item in list:
            print("The text is:  " + item.text)
            self.soft_assert(self.assertEqual,item.text,value)
            if item.text == value:
                print('test_past')
            else:
                print('test_failed')
    def assertItem(self,item,value):
        self.soft_assert(self.assertEqual,item,value)
        if item == value:
            return True
        else:
            return False
    def asset_ge(self,value_1,value_2):
        self.soft_assert(self.assertGreaterEqual,value_1,value_2)

        if value_1 >= value_2:
            return True
        else:
            return False


    def get_account_info(self,role):
        if role == "Sale":
            user_name = 'sale1'
            pass_word = '123456'
        elif role == "Ds":
            user_name = 'ds1'
            pass_word = '123456'
        elif role == "Domestic":
            user_name = 'production1'
            pass_word = '123456'
        elif role == "Export":
            user_name = 'export1'
            pass_word = '123456'
        elif role == "Material":
            user_name = 'material1'
            pass_word = '123456'
        else:
            user_name = 'sale1'
            pass_word = '123456'
        return user_name,pass_word
    @staticmethod
    def generate_chasis_number(test_data_file):
        row_counts = ExcelUtil.getRowCount(test_data_file, sheetName='Sheet1')
        for row_num in range(2, row_counts + 1):
            chassis_number = ExcelUtil.readData(test_data_file, 'Sheet1', row_num, 15)
            if len(chassis_number) < 6:
                random_surffix = random.randint(10000,9999999)
                chassis_number = chassis_number + "-" + str(random_surffix)
                ExcelUtil.writeData(test_data_file,sheetName='Sheet1',row_num=row_num,columnno=15,data=chassis_number)
    @staticmethod
    def generate_random_kanakana(length,katakana_type="full"):
        full_width_katakana = [
            'ア', 'イ', 'ウ', 'エ', 'オ',  # A, I, U, E, O
            'カ', 'キ', 'ク', 'ケ', 'コ',  # KA, KI, KU, KE, KO
            'サ', 'シ', 'ス', 'セ', 'ソ',  # SA, SHI, SU, SE, SO
            'タ', 'チ', 'ツ', 'テ', 'ト',  # TA, CHI, TSU, TE, TO
            'ナ', 'ニ', 'ヌ', 'ネ', 'ノ',  # NA, NI, NU, NE, NO
            'ハ', 'ヒ', 'フ', 'ヘ', 'ホ',  # HA, HI, FU, HE, HO
            'マ', 'ミ', 'ム', 'メ', 'モ',  # MA, MI, MU, ME, MO
            'ヤ', 'ユ', 'ヨ',  # YA, YU, YO
            'ラ', 'リ', 'ル', 'レ', 'ロ',  # RA, RI, RU, RE, RO
            'ワ', 'ヲ', 'ン',  # WA, WO, N
            'ガ', 'ギ', 'グ', 'ゲ', 'ゴ',  # GA, GI, GU, GE, GO
            'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ',  # ZA, JI, ZU, ZE, ZO
            'ダ', 'ヂ', 'ヅ', 'デ', 'ド',  # DA, DJI, DZU, DE, DO
            'バ', 'ビ', 'ブ', 'ベ', 'ボ',  # BA, BI, BU, BE, BO
            'パ', 'ピ', 'プ', 'ペ', 'ポ'  # PA, PI, PU, PE, PO
        ]

        # Half-width katakana (HalfSize) - Unicode range U+FF65 to U+FF9F
        half_width_katakana = [
            'ｱ', 'ｲ', 'ｳ', 'ｴ', 'ｵ',  # A, I, U, E, O
            'ｶ', 'ｷ', 'ｸ', 'ｹ', 'ｺ',  # KA, KI, KU, KE, KO
            'ｻ', 'ｼ', 'ｽ', 'ｾ', 'ｿ',  # SA, SHI, SU, SE, SO
            'ﾀ', 'ﾁ', 'ﾂ', 'ﾃ', 'ﾄ',  # TA, CHI, TSU, TE, TO
            'ﾅ', 'ﾆ', 'ﾇ', 'ﾈ', 'ﾉ',  # NA, NI, NU, NE, NO
            'ﾊ', 'ﾋ', 'ﾌ', 'ﾍ', 'ﾎ',  # HA, HI, FU, HE, HO
            'ﾏ', 'ﾐ', 'ﾑ', 'ﾒ', 'ﾓ',  # MA, MI, MU, ME, MO
            'ﾔ', 'ﾕ', 'ﾖ',  # YA, YU, YO
            'ﾗ', 'ﾘ', 'ﾙ', 'ﾚ', 'ﾛ',  # RA, RI, RU, RE, RO
            'ﾜ', 'ｦ', 'ﾝ'  # WA, WO, N
        ]

        # Select character set based on type
        if katakana_type.lower() == "half":
            char_set = half_width_katakana
        elif katakana_type.lower() == "full":
            char_set = full_width_katakana
        else:
            raise ValueError("katakana_type must be 'full' or 'half'")

        # Generate random string
        return ''.join(random.choices(char_set, k=length))









