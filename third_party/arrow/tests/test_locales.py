import pytest

from arrow import arrow, locales


@pytest.mark.usefixtures("lang_locales")
class TestLocaleValidation:
    """Validate locales to ensure that translations are valid and complete"""

    def test_locale_validation(self):

        for locale_cls in self.locales.values():
            # 7 days + 1 spacer to allow for 1-indexing of months
            assert len(locale_cls.day_names) == 8
            assert locale_cls.day_names[0] == ""
            # ensure that all string from index 1 onward are valid (not blank or None)
            assert all(locale_cls.day_names[1:])

            assert len(locale_cls.day_abbreviations) == 8
            assert locale_cls.day_abbreviations[0] == ""
            assert all(locale_cls.day_abbreviations[1:])

            # 12 months + 1 spacer to allow for 1-indexing of months
            assert len(locale_cls.month_names) == 13
            assert locale_cls.month_names[0] == ""
            assert all(locale_cls.month_names[1:])

            assert len(locale_cls.month_abbreviations) == 13
            assert locale_cls.month_abbreviations[0] == ""
            assert all(locale_cls.month_abbreviations[1:])

            assert len(locale_cls.names) > 0
            assert locale_cls.past is not None
            assert locale_cls.future is not None

    def test_locale_name_validation(self):

        for locale_cls in self.locales.values():
            for locale_name in locale_cls.names:
                assert len(locale_name) == 2 or len(locale_name) == 5
                assert locale_name.islower()
                # Not a two-letter code
                if len(locale_name) > 2:
                    assert "-" in locale_name
                    assert locale_name.count("-") == 1

    def test_duplicated_locale_name(self):
        with pytest.raises(LookupError):

            class Locale1(locales.Locale):
                names = ["en-us"]


class TestModule:
    def test_get_locale(self, mocker):
        mock_locale = mocker.Mock()
        mock_locale_cls = mocker.Mock()
        mock_locale_cls.return_value = mock_locale

        with pytest.raises(ValueError):
            arrow.locales.get_locale("locale-name")

        cls_dict = arrow.locales._locale_map
        mocker.patch.dict(cls_dict, {"locale-name": mock_locale_cls})

        result = arrow.locales.get_locale("locale_name")
        assert result == mock_locale

        # Capitalization and hyphenation should still yield the same locale
        result = arrow.locales.get_locale("locale-name")
        assert result == mock_locale

        result = arrow.locales.get_locale("locale-NAME")
        assert result == mock_locale

    def test_get_locale_by_class_name(self, mocker):
        mock_locale_cls = mocker.Mock()
        mock_locale_obj = mock_locale_cls.return_value = mocker.Mock()

        globals_fn = mocker.Mock()
        globals_fn.return_value = {"NonExistentLocale": mock_locale_cls}

        with pytest.raises(ValueError):
            arrow.locales.get_locale_by_class_name("NonExistentLocale")

        mocker.patch.object(locales, "globals", globals_fn)
        result = arrow.locales.get_locale_by_class_name("NonExistentLocale")

        mock_locale_cls.assert_called_once_with()
        assert result == mock_locale_obj

    def test_locales(self):

        assert len(locales._locale_map) > 0


class TestCustomLocale:
    def test_custom_locale_subclass(self):
        class CustomLocale1(locales.Locale):
            names = ["foo", "foo-BAR"]

        assert locales.get_locale("foo") is not None
        assert locales.get_locale("foo-BAR") is not None
        assert locales.get_locale("foo_bar") is not None

        class CustomLocale2(locales.Locale):
            names = ["underscores_ok"]

        assert locales.get_locale("underscores_ok") is not None


@pytest.mark.usefixtures("lang_locale")
class TestEnglishLocale:
    def test_describe(self):
        assert self.locale.describe("now", only_distance=True) == "instantly"
        assert self.locale.describe("now", only_distance=False) == "just now"

    def test_format_timeframe(self):

        assert self.locale._format_timeframe("hours", 2) == "2 hours"
        assert self.locale._format_timeframe("hour", 0) == "an hour"

    def test_format_relative_now(self):

        result = self.locale._format_relative("just now", "now", 0)

        assert result == "just now"

    def test_format_relative_past(self):

        result = self.locale._format_relative("an hour", "hour", 1)

        assert result == "in an hour"

    def test_format_relative_future(self):

        result = self.locale._format_relative("an hour", "hour", -1)

        assert result == "an hour ago"

    def test_ordinal_number(self):
        assert self.locale.ordinal_number(0) == "0th"
        assert self.locale.ordinal_number(1) == "1st"
        assert self.locale.ordinal_number(2) == "2nd"
        assert self.locale.ordinal_number(3) == "3rd"
        assert self.locale.ordinal_number(4) == "4th"
        assert self.locale.ordinal_number(10) == "10th"
        assert self.locale.ordinal_number(11) == "11th"
        assert self.locale.ordinal_number(12) == "12th"
        assert self.locale.ordinal_number(13) == "13th"
        assert self.locale.ordinal_number(14) == "14th"
        assert self.locale.ordinal_number(21) == "21st"
        assert self.locale.ordinal_number(22) == "22nd"
        assert self.locale.ordinal_number(23) == "23rd"
        assert self.locale.ordinal_number(24) == "24th"

        assert self.locale.ordinal_number(100) == "100th"
        assert self.locale.ordinal_number(101) == "101st"
        assert self.locale.ordinal_number(102) == "102nd"
        assert self.locale.ordinal_number(103) == "103rd"
        assert self.locale.ordinal_number(104) == "104th"
        assert self.locale.ordinal_number(110) == "110th"
        assert self.locale.ordinal_number(111) == "111th"
        assert self.locale.ordinal_number(112) == "112th"
        assert self.locale.ordinal_number(113) == "113th"
        assert self.locale.ordinal_number(114) == "114th"
        assert self.locale.ordinal_number(121) == "121st"
        assert self.locale.ordinal_number(122) == "122nd"
        assert self.locale.ordinal_number(123) == "123rd"
        assert self.locale.ordinal_number(124) == "124th"

    def test_meridian_invalid_token(self):
        assert self.locale.meridian(7, None) is None
        assert self.locale.meridian(7, "B") is None
        assert self.locale.meridian(7, "NONSENSE") is None


@pytest.mark.usefixtures("lang_locale")
class TestItalianLocale:
    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1??"


@pytest.mark.usefixtures("lang_locale")
class TestSpanishLocale:
    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1??"

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "ahora"
        assert self.locale._format_timeframe("seconds", 1) == "1 segundos"
        assert self.locale._format_timeframe("seconds", 3) == "3 segundos"
        assert self.locale._format_timeframe("seconds", 30) == "30 segundos"
        assert self.locale._format_timeframe("minute", 1) == "un minuto"
        assert self.locale._format_timeframe("minutes", 4) == "4 minutos"
        assert self.locale._format_timeframe("minutes", 40) == "40 minutos"
        assert self.locale._format_timeframe("hour", 1) == "una hora"
        assert self.locale._format_timeframe("hours", 5) == "5 horas"
        assert self.locale._format_timeframe("hours", 23) == "23 horas"
        assert self.locale._format_timeframe("day", 1) == "un d??a"
        assert self.locale._format_timeframe("days", 6) == "6 d??as"
        assert self.locale._format_timeframe("days", 12) == "12 d??as"
        assert self.locale._format_timeframe("week", 1) == "una semana"
        assert self.locale._format_timeframe("weeks", 2) == "2 semanas"
        assert self.locale._format_timeframe("weeks", 3) == "3 semanas"
        assert self.locale._format_timeframe("month", 1) == "un mes"
        assert self.locale._format_timeframe("months", 7) == "7 meses"
        assert self.locale._format_timeframe("months", 11) == "11 meses"
        assert self.locale._format_timeframe("year", 1) == "un a??o"
        assert self.locale._format_timeframe("years", 8) == "8 a??os"
        assert self.locale._format_timeframe("years", 12) == "12 a??os"

        assert self.locale._format_timeframe("now", 0) == "ahora"
        assert self.locale._format_timeframe("seconds", -1) == "1 segundos"
        assert self.locale._format_timeframe("seconds", -9) == "9 segundos"
        assert self.locale._format_timeframe("seconds", -12) == "12 segundos"
        assert self.locale._format_timeframe("minute", -1) == "un minuto"
        assert self.locale._format_timeframe("minutes", -2) == "2 minutos"
        assert self.locale._format_timeframe("minutes", -10) == "10 minutos"
        assert self.locale._format_timeframe("hour", -1) == "una hora"
        assert self.locale._format_timeframe("hours", -3) == "3 horas"
        assert self.locale._format_timeframe("hours", -11) == "11 horas"
        assert self.locale._format_timeframe("day", -1) == "un d??a"
        assert self.locale._format_timeframe("days", -2) == "2 d??as"
        assert self.locale._format_timeframe("days", -12) == "12 d??as"
        assert self.locale._format_timeframe("week", -1) == "una semana"
        assert self.locale._format_timeframe("weeks", -2) == "2 semanas"
        assert self.locale._format_timeframe("weeks", -3) == "3 semanas"
        assert self.locale._format_timeframe("month", -1) == "un mes"
        assert self.locale._format_timeframe("months", -3) == "3 meses"
        assert self.locale._format_timeframe("months", -13) == "13 meses"
        assert self.locale._format_timeframe("year", -1) == "un a??o"
        assert self.locale._format_timeframe("years", -4) == "4 a??os"
        assert self.locale._format_timeframe("years", -14) == "14 a??os"


@pytest.mark.usefixtures("lang_locale")
class TestFrenchLocale:
    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1er"
        assert self.locale.ordinal_number(2) == "2e"

    def test_month_abbreviation(self):
        assert "juil" in self.locale.month_abbreviations


@pytest.mark.usefixtures("lang_locale")
class TestFrenchCanadianLocale:
    def test_month_abbreviation(self):
        assert "juill" in self.locale.month_abbreviations


@pytest.mark.usefixtures("lang_locale")
class TestRussianLocale:
    def test_plurals2(self):
        assert self.locale._format_timeframe("hours", 0) == "0 ??????????"
        assert self.locale._format_timeframe("hours", 1) == "1 ??????"
        assert self.locale._format_timeframe("hours", 2) == "2 ????????"
        assert self.locale._format_timeframe("hours", 4) == "4 ????????"
        assert self.locale._format_timeframe("hours", 5) == "5 ??????????"
        assert self.locale._format_timeframe("hours", 21) == "21 ??????"
        assert self.locale._format_timeframe("hours", 22) == "22 ????????"
        assert self.locale._format_timeframe("hours", 25) == "25 ??????????"

        # feminine grammatical gender should be tested separately
        assert self.locale._format_timeframe("minutes", 0) == "0 ??????????"
        assert self.locale._format_timeframe("minutes", 1) == "1 ????????????"
        assert self.locale._format_timeframe("minutes", 2) == "2 ????????????"
        assert self.locale._format_timeframe("minutes", 4) == "4 ????????????"
        assert self.locale._format_timeframe("minutes", 5) == "5 ??????????"
        assert self.locale._format_timeframe("minutes", 21) == "21 ????????????"
        assert self.locale._format_timeframe("minutes", 22) == "22 ????????????"
        assert self.locale._format_timeframe("minutes", 25) == "25 ??????????"


@pytest.mark.usefixtures("lang_locale")
class TestPolishLocale:
    def test_plurals(self):

        assert self.locale._format_timeframe("seconds", 0) == "0 sekund"
        assert self.locale._format_timeframe("second", 1) == "sekund??"
        assert self.locale._format_timeframe("seconds", 2) == "2 sekundy"
        assert self.locale._format_timeframe("seconds", 5) == "5 sekund"
        assert self.locale._format_timeframe("seconds", 21) == "21 sekund"
        assert self.locale._format_timeframe("seconds", 22) == "22 sekundy"
        assert self.locale._format_timeframe("seconds", 25) == "25 sekund"

        assert self.locale._format_timeframe("minutes", 0) == "0 minut"
        assert self.locale._format_timeframe("minute", 1) == "minut??"
        assert self.locale._format_timeframe("minutes", 2) == "2 minuty"
        assert self.locale._format_timeframe("minutes", 5) == "5 minut"
        assert self.locale._format_timeframe("minutes", 21) == "21 minut"
        assert self.locale._format_timeframe("minutes", 22) == "22 minuty"
        assert self.locale._format_timeframe("minutes", 25) == "25 minut"

        assert self.locale._format_timeframe("hours", 0) == "0 godzin"
        assert self.locale._format_timeframe("hour", 1) == "godzin??"
        assert self.locale._format_timeframe("hours", 2) == "2 godziny"
        assert self.locale._format_timeframe("hours", 5) == "5 godzin"
        assert self.locale._format_timeframe("hours", 21) == "21 godzin"
        assert self.locale._format_timeframe("hours", 22) == "22 godziny"
        assert self.locale._format_timeframe("hours", 25) == "25 godzin"

        assert self.locale._format_timeframe("weeks", 0) == "0 tygodni"
        assert self.locale._format_timeframe("week", 1) == "tydzie??"
        assert self.locale._format_timeframe("weeks", 2) == "2 tygodnie"
        assert self.locale._format_timeframe("weeks", 5) == "5 tygodni"
        assert self.locale._format_timeframe("weeks", 21) == "21 tygodni"
        assert self.locale._format_timeframe("weeks", 22) == "22 tygodnie"
        assert self.locale._format_timeframe("weeks", 25) == "25 tygodni"

        assert self.locale._format_timeframe("months", 0) == "0 miesi??cy"
        assert self.locale._format_timeframe("month", 1) == "miesi??c"
        assert self.locale._format_timeframe("months", 2) == "2 miesi??ce"
        assert self.locale._format_timeframe("months", 5) == "5 miesi??cy"
        assert self.locale._format_timeframe("months", 21) == "21 miesi??cy"
        assert self.locale._format_timeframe("months", 22) == "22 miesi??ce"
        assert self.locale._format_timeframe("months", 25) == "25 miesi??cy"

        assert self.locale._format_timeframe("years", 0) == "0 lat"
        assert self.locale._format_timeframe("year", 1) == "rok"
        assert self.locale._format_timeframe("years", 2) == "2 lata"
        assert self.locale._format_timeframe("years", 5) == "5 lat"
        assert self.locale._format_timeframe("years", 21) == "21 lat"
        assert self.locale._format_timeframe("years", 22) == "22 lata"
        assert self.locale._format_timeframe("years", 25) == "25 lat"


@pytest.mark.usefixtures("lang_locale")
class TestIcelandicLocale:
    def test_format_timeframe(self):

        assert self.locale._format_timeframe("now", 0) == "r??tt ?? ??essu"

        assert self.locale._format_timeframe("second", -1) == "sek??ndu"
        assert self.locale._format_timeframe("second", 1) == "sek??ndu"

        assert self.locale._format_timeframe("minute", -1) == "einni m??n??tu"
        assert self.locale._format_timeframe("minute", 1) == "eina m??n??tu"

        assert self.locale._format_timeframe("minutes", -2) == "2 m??n??tum"
        assert self.locale._format_timeframe("minutes", 2) == "2 m??n??tur"

        assert self.locale._format_timeframe("hour", -1) == "einum t??ma"
        assert self.locale._format_timeframe("hour", 1) == "einn t??ma"

        assert self.locale._format_timeframe("hours", -2) == "2 t??mum"
        assert self.locale._format_timeframe("hours", 2) == "2 t??ma"

        assert self.locale._format_timeframe("day", -1) == "einum degi"
        assert self.locale._format_timeframe("day", 1) == "einn dag"

        assert self.locale._format_timeframe("days", -2) == "2 d??gum"
        assert self.locale._format_timeframe("days", 2) == "2 daga"

        assert self.locale._format_timeframe("month", -1) == "einum m??nu??i"
        assert self.locale._format_timeframe("month", 1) == "einn m??nu??"

        assert self.locale._format_timeframe("months", -2) == "2 m??nu??um"
        assert self.locale._format_timeframe("months", 2) == "2 m??nu??i"

        assert self.locale._format_timeframe("year", -1) == "einu ??ri"
        assert self.locale._format_timeframe("year", 1) == "eitt ??r"

        assert self.locale._format_timeframe("years", -2) == "2 ??rum"
        assert self.locale._format_timeframe("years", 2) == "2 ??r"

        with pytest.raises(ValueError):
            self.locale._format_timeframe("years", 0)


@pytest.mark.usefixtures("lang_locale")
class TestMalayalamLocale:
    def test_format_timeframe(self):

        assert self.locale._format_timeframe("hours", 2) == "2 ????????????????????????"
        assert self.locale._format_timeframe("hour", 0) == "????????? ????????????????????????"

    def test_format_relative_now(self):

        result = self.locale._format_relative("??????????????????", "now", 0)

        assert result == "??????????????????"

    def test_format_relative_past(self):

        result = self.locale._format_relative("????????? ????????????????????????", "hour", 1)
        assert result == "????????? ???????????????????????? ????????????"

    def test_format_relative_future(self):

        result = self.locale._format_relative("????????? ????????????????????????", "hour", -1)
        assert result == "????????? ???????????????????????? ??????????????????"


@pytest.mark.usefixtures("lang_locale")
class TestMalteseLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "issa"
        assert self.locale._format_timeframe("second", 1) == "sekonda"
        assert self.locale._format_timeframe("seconds", 30) == "30 sekondi"
        assert self.locale._format_timeframe("minute", 1) == "minuta"
        assert self.locale._format_timeframe("minutes", 4) == "4 minuti"
        assert self.locale._format_timeframe("hour", 1) == "sieg??a"
        assert self.locale._format_timeframe("hours", 2) == "2 sag??tejn"
        assert self.locale._format_timeframe("hours", 4) == "4 sig??at"
        assert self.locale._format_timeframe("day", 1) == "jum"
        assert self.locale._format_timeframe("days", 2) == "2 jumejn"
        assert self.locale._format_timeframe("days", 5) == "5 ijiem"
        assert self.locale._format_timeframe("month", 1) == "xahar"
        assert self.locale._format_timeframe("months", 2) == "2 xahrejn"
        assert self.locale._format_timeframe("months", 7) == "7 xhur"
        assert self.locale._format_timeframe("year", 1) == "sena"
        assert self.locale._format_timeframe("years", 2) == "2 sentejn"
        assert self.locale._format_timeframe("years", 8) == "8 snin"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "Is-Sibt"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "S"


@pytest.mark.usefixtures("lang_locale")
class TestHindiLocale:
    def test_format_timeframe(self):

        assert self.locale._format_timeframe("hours", 2) == "2 ????????????"
        assert self.locale._format_timeframe("hour", 0) == "?????? ????????????"

    def test_format_relative_now(self):

        result = self.locale._format_relative("?????????", "now", 0)
        assert result == "?????????"

    def test_format_relative_past(self):

        result = self.locale._format_relative("?????? ????????????", "hour", 1)
        assert result == "?????? ???????????? ?????????"

    def test_format_relative_future(self):

        result = self.locale._format_relative("?????? ????????????", "hour", -1)
        assert result == "?????? ???????????? ????????????"


@pytest.mark.usefixtures("lang_locale")
class TestCzechLocale:
    def test_format_timeframe(self):

        assert self.locale._format_timeframe("hours", 2) == "2 hodiny"
        assert self.locale._format_timeframe("hours", 5) == "5 hodin"
        assert self.locale._format_timeframe("hour", 0) == "0 hodin"
        assert self.locale._format_timeframe("hours", -2) == "2 hodinami"
        assert self.locale._format_timeframe("hours", -5) == "5 hodinami"
        assert self.locale._format_timeframe("hour", 1) == "hodinu"

        assert self.locale._format_timeframe("now", 0) == "Te??"

        assert self.locale._format_timeframe("weeks", 2) == "2 t??dny"
        assert self.locale._format_timeframe("weeks", 5) == "5 t??dn??"
        assert self.locale._format_timeframe("week", 0) == "0 t??dn??"
        assert self.locale._format_timeframe("weeks", -2) == "2 t??dny"
        assert self.locale._format_timeframe("weeks", -5) == "5 t??dny"

    def test_format_relative_now(self):

        result = self.locale._format_relative("Te??", "now", 0)
        assert result == "Te??"

    def test_format_relative_future(self):

        result = self.locale._format_relative("hodinu", "hour", 1)
        assert result == "Za hodinu"

    def test_format_relative_past(self):

        result = self.locale._format_relative("hodinou", "hour", -1)
        assert result == "P??ed hodinou"


@pytest.mark.usefixtures("lang_locale")
class TestSlovakLocale:
    def test_format_timeframe(self):

        assert self.locale._format_timeframe("seconds", -5) == "5 sekundami"
        assert self.locale._format_timeframe("seconds", -2) == "2 sekundami"
        assert self.locale._format_timeframe("second", -1) == "sekundou"
        assert self.locale._format_timeframe("second", 0) == "0 sek??nd"
        assert self.locale._format_timeframe("second", 1) == "sekundu"
        assert self.locale._format_timeframe("seconds", 2) == "2 sekundy"
        assert self.locale._format_timeframe("seconds", 5) == "5 sek??nd"

        assert self.locale._format_timeframe("minutes", -5) == "5 min??tami"
        assert self.locale._format_timeframe("minutes", -2) == "2 min??tami"
        assert self.locale._format_timeframe("minute", -1) == "min??tou"
        assert self.locale._format_timeframe("minute", 0) == "0 min??t"
        assert self.locale._format_timeframe("minute", 1) == "min??tu"
        assert self.locale._format_timeframe("minutes", 2) == "2 min??ty"
        assert self.locale._format_timeframe("minutes", 5) == "5 min??t"

        assert self.locale._format_timeframe("hours", -5) == "5 hodinami"
        assert self.locale._format_timeframe("hours", -2) == "2 hodinami"
        assert self.locale._format_timeframe("hour", -1) == "hodinou"
        assert self.locale._format_timeframe("hour", 0) == "0 hod??n"
        assert self.locale._format_timeframe("hour", 1) == "hodinu"
        assert self.locale._format_timeframe("hours", 2) == "2 hodiny"
        assert self.locale._format_timeframe("hours", 5) == "5 hod??n"

        assert self.locale._format_timeframe("days", -5) == "5 d??ami"
        assert self.locale._format_timeframe("days", -2) == "2 d??ami"
        assert self.locale._format_timeframe("day", -1) == "d??om"
        assert self.locale._format_timeframe("day", 0) == "0 dn??"
        assert self.locale._format_timeframe("day", 1) == "de??"
        assert self.locale._format_timeframe("days", 2) == "2 dni"
        assert self.locale._format_timeframe("days", 5) == "5 dn??"

        assert self.locale._format_timeframe("weeks", -5) == "5 t????d??ami"
        assert self.locale._format_timeframe("weeks", -2) == "2 t????d??ami"
        assert self.locale._format_timeframe("week", -1) == "t????d??om"
        assert self.locale._format_timeframe("week", 0) == "0 t????d??ov"
        assert self.locale._format_timeframe("week", 1) == "t????de??"
        assert self.locale._format_timeframe("weeks", 2) == "2 t????dne"
        assert self.locale._format_timeframe("weeks", 5) == "5 t????d??ov"

        assert self.locale._format_timeframe("months", -5) == "5 mesiacmi"
        assert self.locale._format_timeframe("months", -2) == "2 mesiacmi"
        assert self.locale._format_timeframe("month", -1) == "mesiacom"
        assert self.locale._format_timeframe("month", 0) == "0 mesiacov"
        assert self.locale._format_timeframe("month", 1) == "mesiac"
        assert self.locale._format_timeframe("months", 2) == "2 mesiace"
        assert self.locale._format_timeframe("months", 5) == "5 mesiacov"

        assert self.locale._format_timeframe("years", -5) == "5 rokmi"
        assert self.locale._format_timeframe("years", -2) == "2 rokmi"
        assert self.locale._format_timeframe("year", -1) == "rokom"
        assert self.locale._format_timeframe("year", 0) == "0 rokov"
        assert self.locale._format_timeframe("year", 1) == "rok"
        assert self.locale._format_timeframe("years", 2) == "2 roky"
        assert self.locale._format_timeframe("years", 5) == "5 rokov"

        assert self.locale._format_timeframe("now", 0) == "Teraz"

    def test_format_relative_now(self):

        result = self.locale._format_relative("Teraz", "now", 0)
        assert result == "Teraz"

    def test_format_relative_future(self):

        result = self.locale._format_relative("hodinu", "hour", 1)
        assert result == "O hodinu"

    def test_format_relative_past(self):

        result = self.locale._format_relative("hodinou", "hour", -1)
        assert result == "Pred hodinou"


@pytest.mark.usefixtures("lang_locale")
class TestBulgarianLocale:
    def test_plurals2(self):
        assert self.locale._format_timeframe("hours", 0) == "0 ????????"
        assert self.locale._format_timeframe("hours", 1) == "1 ??????"
        assert self.locale._format_timeframe("hours", 2) == "2 ????????"
        assert self.locale._format_timeframe("hours", 4) == "4 ????????"
        assert self.locale._format_timeframe("hours", 5) == "5 ????????"
        assert self.locale._format_timeframe("hours", 21) == "21 ??????"
        assert self.locale._format_timeframe("hours", 22) == "22 ????????"
        assert self.locale._format_timeframe("hours", 25) == "25 ????????"

        # feminine grammatical gender should be tested separately
        assert self.locale._format_timeframe("minutes", 0) == "0 ????????????"
        assert self.locale._format_timeframe("minutes", 1) == "1 ????????????"
        assert self.locale._format_timeframe("minutes", 2) == "2 ????????????"
        assert self.locale._format_timeframe("minutes", 4) == "4 ????????????"
        assert self.locale._format_timeframe("minutes", 5) == "5 ????????????"
        assert self.locale._format_timeframe("minutes", 21) == "21 ????????????"
        assert self.locale._format_timeframe("minutes", 22) == "22 ????????????"
        assert self.locale._format_timeframe("minutes", 25) == "25 ????????????"


@pytest.mark.usefixtures("lang_locale")
class TestMacedonianLocale:
    def test_singles_mk(self):
        assert self.locale._format_timeframe("second", 1) == "???????? ??????????????"
        assert self.locale._format_timeframe("minute", 1) == "???????? ????????????"
        assert self.locale._format_timeframe("hour", 1) == "???????? ????????"
        assert self.locale._format_timeframe("day", 1) == "???????? ??????"
        assert self.locale._format_timeframe("week", 1) == "???????? ????????????"
        assert self.locale._format_timeframe("month", 1) == "???????? ??????????"
        assert self.locale._format_timeframe("year", 1) == "???????? ????????????"

    def test_meridians_mk(self):
        assert self.locale.meridian(7, "A") == "????????????????????"
        assert self.locale.meridian(18, "A") == "????????????????"
        assert self.locale.meridian(10, "a") == "????"
        assert self.locale.meridian(22, "a") == "????"

    def test_describe_mk(self):
        assert self.locale.describe("second", only_distance=True) == "???????? ??????????????"
        assert self.locale.describe("second", only_distance=False) == "???? ???????? ??????????????"
        assert self.locale.describe("minute", only_distance=True) == "???????? ????????????"
        assert self.locale.describe("minute", only_distance=False) == "???? ???????? ????????????"
        assert self.locale.describe("hour", only_distance=True) == "???????? ????????"
        assert self.locale.describe("hour", only_distance=False) == "???? ???????? ????????"
        assert self.locale.describe("day", only_distance=True) == "???????? ??????"
        assert self.locale.describe("day", only_distance=False) == "???? ???????? ??????"
        assert self.locale.describe("week", only_distance=True) == "???????? ????????????"
        assert self.locale.describe("week", only_distance=False) == "???? ???????? ????????????"
        assert self.locale.describe("month", only_distance=True) == "???????? ??????????"
        assert self.locale.describe("month", only_distance=False) == "???? ???????? ??????????"
        assert self.locale.describe("year", only_distance=True) == "???????? ????????????"
        assert self.locale.describe("year", only_distance=False) == "???? ???????? ????????????"

    def test_relative_mk(self):
        # time
        assert self.locale._format_relative("????????", "now", 0) == "????????"
        assert self.locale._format_relative("1 ??????????????", "seconds", 1) == "???? 1 ??????????????"
        assert self.locale._format_relative("1 ????????????", "minutes", 1) == "???? 1 ????????????"
        assert self.locale._format_relative("1 ????????", "hours", 1) == "???? 1 ????????"
        assert self.locale._format_relative("1 ??????", "days", 1) == "???? 1 ??????"
        assert self.locale._format_relative("1 ????????????", "weeks", 1) == "???? 1 ????????????"
        assert self.locale._format_relative("1 ??????????", "months", 1) == "???? 1 ??????????"
        assert self.locale._format_relative("1 ????????????", "years", 1) == "???? 1 ????????????"
        assert (
            self.locale._format_relative("1 ??????????????", "seconds", -1) == "???????? 1 ??????????????"
        )
        assert (
            self.locale._format_relative("1 ????????????", "minutes", -1) == "???????? 1 ????????????"
        )
        assert self.locale._format_relative("1 ????????", "hours", -1) == "???????? 1 ????????"
        assert self.locale._format_relative("1 ??????", "days", -1) == "???????? 1 ??????"
        assert self.locale._format_relative("1 ????????????", "weeks", -1) == "???????? 1 ????????????"
        assert self.locale._format_relative("1 ??????????", "months", -1) == "???????? 1 ??????????"
        assert self.locale._format_relative("1 ????????????", "years", -1) == "???????? 1 ????????????"

    def test_plurals_mk(self):
        # Seconds
        assert self.locale._format_timeframe("seconds", 0) == "0 ??????????????"
        assert self.locale._format_timeframe("seconds", 1) == "1 ??????????????"
        assert self.locale._format_timeframe("seconds", 2) == "2 ??????????????"
        assert self.locale._format_timeframe("seconds", 4) == "4 ??????????????"
        assert self.locale._format_timeframe("seconds", 5) == "5 ??????????????"
        assert self.locale._format_timeframe("seconds", 21) == "21 ??????????????"
        assert self.locale._format_timeframe("seconds", 22) == "22 ??????????????"
        assert self.locale._format_timeframe("seconds", 25) == "25 ??????????????"

        # Minutes
        assert self.locale._format_timeframe("minutes", 0) == "0 ????????????"
        assert self.locale._format_timeframe("minutes", 1) == "1 ????????????"
        assert self.locale._format_timeframe("minutes", 2) == "2 ????????????"
        assert self.locale._format_timeframe("minutes", 4) == "4 ????????????"
        assert self.locale._format_timeframe("minutes", 5) == "5 ????????????"
        assert self.locale._format_timeframe("minutes", 21) == "21 ????????????"
        assert self.locale._format_timeframe("minutes", 22) == "22 ????????????"
        assert self.locale._format_timeframe("minutes", 25) == "25 ????????????"

        # Hours
        assert self.locale._format_timeframe("hours", 0) == "0 ??????????"
        assert self.locale._format_timeframe("hours", 1) == "1 ????????"
        assert self.locale._format_timeframe("hours", 2) == "2 ??????????"
        assert self.locale._format_timeframe("hours", 4) == "4 ??????????"
        assert self.locale._format_timeframe("hours", 5) == "5 ??????????"
        assert self.locale._format_timeframe("hours", 21) == "21 ????????"
        assert self.locale._format_timeframe("hours", 22) == "22 ??????????"
        assert self.locale._format_timeframe("hours", 25) == "25 ??????????"

        # Days
        assert self.locale._format_timeframe("days", 0) == "0 ????????"
        assert self.locale._format_timeframe("days", 1) == "1 ??????"
        assert self.locale._format_timeframe("days", 2) == "2 ????????"
        assert self.locale._format_timeframe("days", 3) == "3 ????????"
        assert self.locale._format_timeframe("days", 21) == "21 ??????"

        # Weeks
        assert self.locale._format_timeframe("weeks", 0) == "0 ????????????"
        assert self.locale._format_timeframe("weeks", 1) == "1 ????????????"
        assert self.locale._format_timeframe("weeks", 2) == "2 ????????????"
        assert self.locale._format_timeframe("weeks", 4) == "4 ????????????"
        assert self.locale._format_timeframe("weeks", 5) == "5 ????????????"
        assert self.locale._format_timeframe("weeks", 21) == "21 ????????????"
        assert self.locale._format_timeframe("weeks", 22) == "22 ????????????"
        assert self.locale._format_timeframe("weeks", 25) == "25 ????????????"

        # Months
        assert self.locale._format_timeframe("months", 0) == "0 ????????????"
        assert self.locale._format_timeframe("months", 1) == "1 ??????????"
        assert self.locale._format_timeframe("months", 2) == "2 ????????????"
        assert self.locale._format_timeframe("months", 4) == "4 ????????????"
        assert self.locale._format_timeframe("months", 5) == "5 ????????????"
        assert self.locale._format_timeframe("months", 21) == "21 ??????????"
        assert self.locale._format_timeframe("months", 22) == "22 ????????????"
        assert self.locale._format_timeframe("months", 25) == "25 ????????????"

        # Years
        assert self.locale._format_timeframe("years", 1) == "1 ????????????"
        assert self.locale._format_timeframe("years", 2) == "2 ????????????"
        assert self.locale._format_timeframe("years", 5) == "5 ????????????"

    def test_multi_describe_mk(self):
        describe = self.locale.describe_multi

        fulltest = [("years", 5), ("weeks", 1), ("hours", 1), ("minutes", 6)]
        assert describe(fulltest) == "???? 5 ???????????? 1 ???????????? 1 ???????? 6 ????????????"
        seconds4000_0days = [("days", 0), ("hours", 1), ("minutes", 6)]
        assert describe(seconds4000_0days) == "???? 0 ???????? 1 ???????? 6 ????????????"
        seconds4000 = [("hours", 1), ("minutes", 6)]
        assert describe(seconds4000) == "???? 1 ???????? 6 ????????????"
        assert describe(seconds4000, only_distance=True) == "1 ???????? 6 ????????????"
        seconds3700 = [("hours", 1), ("minutes", 1)]
        assert describe(seconds3700) == "???? 1 ???????? 1 ????????????"
        seconds300_0hours = [("hours", 0), ("minutes", 5)]
        assert describe(seconds300_0hours) == "???? 0 ?????????? 5 ????????????"
        seconds300 = [("minutes", 5)]
        assert describe(seconds300) == "???? 5 ????????????"
        seconds60 = [("minutes", 1)]
        assert describe(seconds60) == "???? 1 ????????????"
        assert describe(seconds60, only_distance=True) == "1 ????????????"
        seconds60 = [("seconds", 1)]
        assert describe(seconds60) == "???? 1 ??????????????"
        assert describe(seconds60, only_distance=True) == "1 ??????????????"


@pytest.mark.usefixtures("time_2013_01_01")
@pytest.mark.usefixtures("lang_locale")
class TestHebrewLocale:
    def test_couple_of_timeframe(self):
        assert self.locale._format_timeframe("day", 1) == "??????"
        assert self.locale._format_timeframe("days", 2) == "????????????"
        assert self.locale._format_timeframe("days", 3) == "3 ????????"
        assert self.locale._format_timeframe("days", 80) == "80 ??????"

        assert self.locale._format_timeframe("hour", 1) == "??????"
        assert self.locale._format_timeframe("hours", 2) == "????????????"
        assert self.locale._format_timeframe("hours", 3) == "3 ????????"

        assert self.locale._format_timeframe("week", 1) == "????????"
        assert self.locale._format_timeframe("weeks", 2) == "??????????????"
        assert self.locale._format_timeframe("weeks", 3) == "3 ????????????"

        assert self.locale._format_timeframe("month", 1) == "????????"
        assert self.locale._format_timeframe("months", 2) == "??????????????"
        assert self.locale._format_timeframe("months", 4) == "4 ????????????"

        assert self.locale._format_timeframe("year", 1) == "??????"
        assert self.locale._format_timeframe("years", 2) == "????????????"
        assert self.locale._format_timeframe("years", 5) == "5 ????????"
        assert self.locale._format_timeframe("years", 15) == "15 ??????"

    def test_describe_multi(self):
        describe = self.locale.describe_multi

        fulltest = [("years", 5), ("week", 1), ("hour", 1), ("minutes", 6)]
        assert describe(fulltest) == "???????? 5 ????????, ????????, ?????? ????6 ????????"
        seconds4000_0days = [("days", 0), ("hour", 1), ("minutes", 6)]
        assert describe(seconds4000_0days) == "???????? 0 ????????, ?????? ????6 ????????"
        seconds4000 = [("hour", 1), ("minutes", 6)]
        assert describe(seconds4000) == "???????? ?????? ????6 ????????"
        assert describe(seconds4000, only_distance=True) == "?????? ????6 ????????"
        seconds3700 = [("hour", 1), ("minute", 1)]
        assert describe(seconds3700) == "???????? ?????? ????????"
        seconds300_0hours = [("hours", 0), ("minutes", 5)]
        assert describe(seconds300_0hours) == "???????? 0 ???????? ????5 ????????"
        seconds300 = [("minutes", 5)]
        assert describe(seconds300) == "???????? 5 ????????"
        seconds60 = [("minute", 1)]
        assert describe(seconds60) == "???????? ??????"
        assert describe(seconds60, only_distance=True) == "??????"


@pytest.mark.usefixtures("lang_locale")
class TestAzerbaijaniLocale:
    def test_singles_mk(self):
        assert self.locale._format_timeframe("second", 1) == "bir saniy??"
        assert self.locale._format_timeframe("minute", 1) == "bir d??qiq??"
        assert self.locale._format_timeframe("hour", 1) == "bir saat"
        assert self.locale._format_timeframe("day", 1) == "bir g??n"
        assert self.locale._format_timeframe("week", 1) == "bir h??ft??"
        assert self.locale._format_timeframe("month", 1) == "bir ay"
        assert self.locale._format_timeframe("year", 1) == "bir il"

    def test_describe_mk(self):
        assert self.locale.describe("second", only_distance=True) == "bir saniy??"
        assert self.locale.describe("second", only_distance=False) == "bir saniy?? sonra"
        assert self.locale.describe("minute", only_distance=True) == "bir d??qiq??"
        assert self.locale.describe("minute", only_distance=False) == "bir d??qiq?? sonra"
        assert self.locale.describe("hour", only_distance=True) == "bir saat"
        assert self.locale.describe("hour", only_distance=False) == "bir saat sonra"
        assert self.locale.describe("day", only_distance=True) == "bir g??n"
        assert self.locale.describe("day", only_distance=False) == "bir g??n sonra"
        assert self.locale.describe("week", only_distance=True) == "bir h??ft??"
        assert self.locale.describe("week", only_distance=False) == "bir h??ft?? sonra"
        assert self.locale.describe("month", only_distance=True) == "bir ay"
        assert self.locale.describe("month", only_distance=False) == "bir ay sonra"
        assert self.locale.describe("year", only_distance=True) == "bir il"
        assert self.locale.describe("year", only_distance=False) == "bir il sonra"

    def test_relative_mk(self):
        assert self.locale._format_relative("indi", "now", 0) == "indi"
        assert (
            self.locale._format_relative("1 saniy??", "seconds", 1) == "1 saniy?? sonra"
        )
        assert (
            self.locale._format_relative("1 saniy??", "seconds", -1) == "1 saniy?? ??vv??l"
        )
        assert (
            self.locale._format_relative("1 d??qiq??", "minutes", 1) == "1 d??qiq?? sonra"
        )
        assert (
            self.locale._format_relative("1 d??qiq??", "minutes", -1) == "1 d??qiq?? ??vv??l"
        )
        assert self.locale._format_relative("1 saat", "hours", 1) == "1 saat sonra"
        assert self.locale._format_relative("1 saat", "hours", -1) == "1 saat ??vv??l"
        assert self.locale._format_relative("1 g??n", "days", 1) == "1 g??n sonra"
        assert self.locale._format_relative("1 g??n", "days", -1) == "1 g??n ??vv??l"
        assert self.locale._format_relative("1 hafta", "weeks", 1) == "1 hafta sonra"
        assert self.locale._format_relative("1 hafta", "weeks", -1) == "1 hafta ??vv??l"
        assert self.locale._format_relative("1 ay", "months", 1) == "1 ay sonra"
        assert self.locale._format_relative("1 ay", "months", -1) == "1 ay ??vv??l"
        assert self.locale._format_relative("1 il", "years", 1) == "1 il sonra"
        assert self.locale._format_relative("1 il", "years", -1) == "1 il ??vv??l"

    def test_plurals_mk(self):
        assert self.locale._format_timeframe("now", 0) == "indi"
        assert self.locale._format_timeframe("second", 1) == "bir saniy??"
        assert self.locale._format_timeframe("seconds", 30) == "30 saniy??"
        assert self.locale._format_timeframe("minute", 1) == "bir d??qiq??"
        assert self.locale._format_timeframe("minutes", 40) == "40 d??qiq??"
        assert self.locale._format_timeframe("hour", 1) == "bir saat"
        assert self.locale._format_timeframe("hours", 23) == "23 saat"
        assert self.locale._format_timeframe("day", 1) == "bir g??n"
        assert self.locale._format_timeframe("days", 12) == "12 g??n"
        assert self.locale._format_timeframe("week", 1) == "bir h??ft??"
        assert self.locale._format_timeframe("weeks", 38) == "38 h??ft??"
        assert self.locale._format_timeframe("month", 1) == "bir ay"
        assert self.locale._format_timeframe("months", 11) == "11 ay"
        assert self.locale._format_timeframe("year", 1) == "bir il"
        assert self.locale._format_timeframe("years", 12) == "12 il"


@pytest.mark.usefixtures("lang_locale")
class TestMarathiLocale:
    def test_dateCoreFunctionality(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.month_name(dt.month) == "??????????????????"
        assert self.locale.month_abbreviation(dt.month) == "???????????????"
        assert self.locale.day_name(dt.isoweekday()) == "??????????????????"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "?????????"

    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", 2) == "2 ?????????"
        assert self.locale._format_timeframe("hour", 0) == "?????? ?????????"

    def test_format_relative_now(self):
        result = self.locale._format_relative("????????????", "now", 0)
        assert result == "????????????"

    def test_format_relative_past(self):
        result = self.locale._format_relative("?????? ?????????", "hour", 1)
        assert result == "?????? ????????? ????????????"

    def test_format_relative_future(self):
        result = self.locale._format_relative("?????? ?????????", "hour", -1)
        assert result == "?????? ????????? ?????????"

    # Not currently implemented
    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1"


@pytest.mark.usefixtures("lang_locale")
class TestFinnishLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", -2) == "2 tuntia"
        assert self.locale._format_timeframe("hours", 2) == "2 tunnin"

        assert self.locale._format_timeframe("hour", -1) == "tunti"
        assert self.locale._format_timeframe("hour", 1) == "tunnin"

        assert self.locale._format_timeframe("now", 1) == "juuri nyt"

    def test_format_relative_now(self):
        result = self.locale._format_relative("juuri nyt", "now", 0)
        assert result == "juuri nyt"

    def test_format_relative_past(self):
        result = self.locale._format_relative("tunnin", "hour", 1)
        assert result == "tunnin kuluttua"

    def test_format_relative_future(self):
        result = self.locale._format_relative("tunti", "hour", -1)
        assert result == "tunti sitten"

    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1."


@pytest.mark.usefixtures("lang_locale")
class TestGermanLocale:
    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1."

    def test_define(self):
        assert self.locale.describe("minute", only_distance=True) == "eine Minute"
        assert self.locale.describe("minute", only_distance=False) == "in einer Minute"
        assert self.locale.describe("hour", only_distance=True) == "eine Stunde"
        assert self.locale.describe("hour", only_distance=False) == "in einer Stunde"
        assert self.locale.describe("day", only_distance=True) == "ein Tag"
        assert self.locale.describe("day", only_distance=False) == "in einem Tag"
        assert self.locale.describe("week", only_distance=True) == "eine Woche"
        assert self.locale.describe("week", only_distance=False) == "in einer Woche"
        assert self.locale.describe("month", only_distance=True) == "ein Monat"
        assert self.locale.describe("month", only_distance=False) == "in einem Monat"
        assert self.locale.describe("year", only_distance=True) == "ein Jahr"
        assert self.locale.describe("year", only_distance=False) == "in einem Jahr"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "Samstag"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "Sa"


@pytest.mark.usefixtures("lang_locale")
class TestHungarianLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", 2) == "2 ??ra"
        assert self.locale._format_timeframe("hour", 0) == "egy ??r??val"
        assert self.locale._format_timeframe("hours", -2) == "2 ??r??val"
        assert self.locale._format_timeframe("now", 0) == "??ppen most"


@pytest.mark.usefixtures("lang_locale")
class TestEsperantoLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", 2) == "2 horoj"
        assert self.locale._format_timeframe("hour", 0) == "un horo"
        assert self.locale._format_timeframe("hours", -2) == "2 horoj"
        assert self.locale._format_timeframe("now", 0) == "nun"

    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1a"


@pytest.mark.usefixtures("lang_locale")
class TestThaiLocale:
    def test_year_full(self):
        assert self.locale.year_full(2015) == "2558"

    def test_year_abbreviation(self):
        assert self.locale.year_abbreviation(2015) == "58"

    def test_format_relative_now(self):
        result = self.locale._format_relative("??????????????????", "now", 0)
        assert result == "??????????????????"

    def test_format_relative_past(self):
        result = self.locale._format_relative("1 ?????????????????????", "hour", 1)
        assert result == "??????????????? 1 ?????????????????????"
        result = self.locale._format_relative("{0} ?????????????????????", "hours", 2)
        assert result == "??????????????? {0} ?????????????????????"
        result = self.locale._format_relative("????????????????????????????????????", "seconds", 42)
        assert result == "???????????????????????????????????????????????????"

    def test_format_relative_future(self):
        result = self.locale._format_relative("1 ?????????????????????", "hour", -1)
        assert result == "1 ????????????????????? ???????????????????????????"


@pytest.mark.usefixtures("lang_locale")
class TestBengaliLocale:
    def test_ordinal_number(self):
        assert self.locale._ordinal_number(0) == "0??????"
        assert self.locale._ordinal_number(1) == "1???"
        assert self.locale._ordinal_number(3) == "3??????"
        assert self.locale._ordinal_number(4) == "4?????????"
        assert self.locale._ordinal_number(5) == "5???"
        assert self.locale._ordinal_number(6) == "6?????????"
        assert self.locale._ordinal_number(10) == "10???"
        assert self.locale._ordinal_number(11) == "11??????"
        assert self.locale._ordinal_number(42) == "42??????"
        assert self.locale._ordinal_number(-1) is None


@pytest.mark.usefixtures("lang_locale")
class TestRomanianLocale:
    def test_timeframes(self):

        assert self.locale._format_timeframe("hours", 2) == "2 ore"
        assert self.locale._format_timeframe("months", 2) == "2 luni"

        assert self.locale._format_timeframe("days", 2) == "2 zile"
        assert self.locale._format_timeframe("years", 2) == "2 ani"

        assert self.locale._format_timeframe("hours", 3) == "3 ore"
        assert self.locale._format_timeframe("months", 4) == "4 luni"
        assert self.locale._format_timeframe("days", 3) == "3 zile"
        assert self.locale._format_timeframe("years", 5) == "5 ani"

    def test_relative_timeframes(self):
        assert self.locale._format_relative("acum", "now", 0) == "acum"
        assert self.locale._format_relative("o or??", "hour", 1) == "peste o or??"
        assert self.locale._format_relative("o or??", "hour", -1) == "o or?? ??n urm??"
        assert self.locale._format_relative("un minut", "minute", 1) == "peste un minut"
        assert (
            self.locale._format_relative("un minut", "minute", -1) == "un minut ??n urm??"
        )
        assert (
            self.locale._format_relative("c??teva secunde", "seconds", -1)
            == "c??teva secunde ??n urm??"
        )
        assert (
            self.locale._format_relative("c??teva secunde", "seconds", 1)
            == "peste c??teva secunde"
        )
        assert self.locale._format_relative("o zi", "day", -1) == "o zi ??n urm??"
        assert self.locale._format_relative("o zi", "day", 1) == "peste o zi"


@pytest.mark.usefixtures("lang_locale")
class TestArabicLocale:
    def test_timeframes(self):

        # single
        assert self.locale._format_timeframe("minute", 1) == "??????????"
        assert self.locale._format_timeframe("hour", 1) == "????????"
        assert self.locale._format_timeframe("day", 1) == "??????"
        assert self.locale._format_timeframe("month", 1) == "??????"
        assert self.locale._format_timeframe("year", 1) == "??????"

        # double
        assert self.locale._format_timeframe("minutes", 2) == "??????????????"
        assert self.locale._format_timeframe("hours", 2) == "????????????"
        assert self.locale._format_timeframe("days", 2) == "??????????"
        assert self.locale._format_timeframe("months", 2) == "??????????"
        assert self.locale._format_timeframe("years", 2) == "??????????"

        # up to ten
        assert self.locale._format_timeframe("minutes", 3) == "3 ??????????"
        assert self.locale._format_timeframe("hours", 4) == "4 ??????????"
        assert self.locale._format_timeframe("days", 5) == "5 ????????"
        assert self.locale._format_timeframe("months", 6) == "6 ????????"
        assert self.locale._format_timeframe("years", 10) == "10 ??????????"

        # more than ten
        assert self.locale._format_timeframe("minutes", 11) == "11 ??????????"
        assert self.locale._format_timeframe("hours", 19) == "19 ????????"
        assert self.locale._format_timeframe("months", 24) == "24 ??????"
        assert self.locale._format_timeframe("days", 50) == "50 ??????"
        assert self.locale._format_timeframe("years", 115) == "115 ??????"


@pytest.mark.usefixtures("lang_locale")
class TestNepaliLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("hours", 3) == "3 ???????????????"
        assert self.locale._format_timeframe("hour", 0) == "?????? ???????????????"

    def test_format_relative_now(self):
        result = self.locale._format_relative("???????????????", "now", 0)
        assert result == "???????????????"

    def test_format_relative_future(self):
        result = self.locale._format_relative("?????? ???????????????", "hour", 1)
        assert result == "?????? ??????????????? ?????????"

    def test_format_relative_past(self):
        result = self.locale._format_relative("?????? ???????????????", "hour", -1)
        assert result == "?????? ??????????????? ???????????????"


@pytest.mark.usefixtures("lang_locale")
class TestIndonesianLocale:
    def test_timeframes(self):
        assert self.locale._format_timeframe("hours", 2) == "2 jam"
        assert self.locale._format_timeframe("months", 2) == "2 bulan"

        assert self.locale._format_timeframe("days", 2) == "2 hari"
        assert self.locale._format_timeframe("years", 2) == "2 tahun"

        assert self.locale._format_timeframe("hours", 3) == "3 jam"
        assert self.locale._format_timeframe("months", 4) == "4 bulan"
        assert self.locale._format_timeframe("days", 3) == "3 hari"
        assert self.locale._format_timeframe("years", 5) == "5 tahun"

    def test_format_relative_now(self):
        assert self.locale._format_relative("baru saja", "now", 0) == "baru saja"

    def test_format_relative_past(self):
        assert self.locale._format_relative("1 jam", "hour", 1) == "dalam 1 jam"
        assert self.locale._format_relative("1 detik", "seconds", 1) == "dalam 1 detik"

    def test_format_relative_future(self):
        assert self.locale._format_relative("1 jam", "hour", -1) == "1 jam yang lalu"


@pytest.mark.usefixtures("lang_locale")
class TestTagalogLocale:
    def test_singles_tl(self):
        assert self.locale._format_timeframe("second", 1) == "isang segundo"
        assert self.locale._format_timeframe("minute", 1) == "isang minuto"
        assert self.locale._format_timeframe("hour", 1) == "isang oras"
        assert self.locale._format_timeframe("day", 1) == "isang araw"
        assert self.locale._format_timeframe("week", 1) == "isang linggo"
        assert self.locale._format_timeframe("month", 1) == "isang buwan"
        assert self.locale._format_timeframe("year", 1) == "isang taon"

    def test_meridians_tl(self):
        assert self.locale.meridian(7, "A") == "ng umaga"
        assert self.locale.meridian(18, "A") == "ng hapon"
        assert self.locale.meridian(10, "a") == "nu"
        assert self.locale.meridian(22, "a") == "nh"

    def test_describe_tl(self):
        assert self.locale.describe("second", only_distance=True) == "isang segundo"
        assert (
            self.locale.describe("second", only_distance=False)
            == "isang segundo mula ngayon"
        )
        assert self.locale.describe("minute", only_distance=True) == "isang minuto"
        assert (
            self.locale.describe("minute", only_distance=False)
            == "isang minuto mula ngayon"
        )
        assert self.locale.describe("hour", only_distance=True) == "isang oras"
        assert (
            self.locale.describe("hour", only_distance=False)
            == "isang oras mula ngayon"
        )
        assert self.locale.describe("day", only_distance=True) == "isang araw"
        assert (
            self.locale.describe("day", only_distance=False) == "isang araw mula ngayon"
        )
        assert self.locale.describe("week", only_distance=True) == "isang linggo"
        assert (
            self.locale.describe("week", only_distance=False)
            == "isang linggo mula ngayon"
        )
        assert self.locale.describe("month", only_distance=True) == "isang buwan"
        assert (
            self.locale.describe("month", only_distance=False)
            == "isang buwan mula ngayon"
        )
        assert self.locale.describe("year", only_distance=True) == "isang taon"
        assert (
            self.locale.describe("year", only_distance=False)
            == "isang taon mula ngayon"
        )

    def test_relative_tl(self):
        # time
        assert self.locale._format_relative("ngayon", "now", 0) == "ngayon"
        assert (
            self.locale._format_relative("1 segundo", "seconds", 1)
            == "1 segundo mula ngayon"
        )
        assert (
            self.locale._format_relative("1 minuto", "minutes", 1)
            == "1 minuto mula ngayon"
        )
        assert (
            self.locale._format_relative("1 oras", "hours", 1) == "1 oras mula ngayon"
        )
        assert self.locale._format_relative("1 araw", "days", 1) == "1 araw mula ngayon"
        assert (
            self.locale._format_relative("1 linggo", "weeks", 1)
            == "1 linggo mula ngayon"
        )
        assert (
            self.locale._format_relative("1 buwan", "months", 1)
            == "1 buwan mula ngayon"
        )
        assert (
            self.locale._format_relative("1 taon", "years", 1) == "1 taon mula ngayon"
        )
        assert (
            self.locale._format_relative("1 segundo", "seconds", -1)
            == "nakaraang 1 segundo"
        )
        assert (
            self.locale._format_relative("1 minuto", "minutes", -1)
            == "nakaraang 1 minuto"
        )
        assert self.locale._format_relative("1 oras", "hours", -1) == "nakaraang 1 oras"
        assert self.locale._format_relative("1 araw", "days", -1) == "nakaraang 1 araw"
        assert (
            self.locale._format_relative("1 linggo", "weeks", -1)
            == "nakaraang 1 linggo"
        )
        assert (
            self.locale._format_relative("1 buwan", "months", -1) == "nakaraang 1 buwan"
        )
        assert self.locale._format_relative("1 taon", "years", -1) == "nakaraang 1 taon"

    def test_plurals_tl(self):
        # Seconds
        assert self.locale._format_timeframe("seconds", 0) == "0 segundo"
        assert self.locale._format_timeframe("seconds", 1) == "1 segundo"
        assert self.locale._format_timeframe("seconds", 2) == "2 segundo"
        assert self.locale._format_timeframe("seconds", 4) == "4 segundo"
        assert self.locale._format_timeframe("seconds", 5) == "5 segundo"
        assert self.locale._format_timeframe("seconds", 21) == "21 segundo"
        assert self.locale._format_timeframe("seconds", 22) == "22 segundo"
        assert self.locale._format_timeframe("seconds", 25) == "25 segundo"

        # Minutes
        assert self.locale._format_timeframe("minutes", 0) == "0 minuto"
        assert self.locale._format_timeframe("minutes", 1) == "1 minuto"
        assert self.locale._format_timeframe("minutes", 2) == "2 minuto"
        assert self.locale._format_timeframe("minutes", 4) == "4 minuto"
        assert self.locale._format_timeframe("minutes", 5) == "5 minuto"
        assert self.locale._format_timeframe("minutes", 21) == "21 minuto"
        assert self.locale._format_timeframe("minutes", 22) == "22 minuto"
        assert self.locale._format_timeframe("minutes", 25) == "25 minuto"

        # Hours
        assert self.locale._format_timeframe("hours", 0) == "0 oras"
        assert self.locale._format_timeframe("hours", 1) == "1 oras"
        assert self.locale._format_timeframe("hours", 2) == "2 oras"
        assert self.locale._format_timeframe("hours", 4) == "4 oras"
        assert self.locale._format_timeframe("hours", 5) == "5 oras"
        assert self.locale._format_timeframe("hours", 21) == "21 oras"
        assert self.locale._format_timeframe("hours", 22) == "22 oras"
        assert self.locale._format_timeframe("hours", 25) == "25 oras"

        # Days
        assert self.locale._format_timeframe("days", 0) == "0 araw"
        assert self.locale._format_timeframe("days", 1) == "1 araw"
        assert self.locale._format_timeframe("days", 2) == "2 araw"
        assert self.locale._format_timeframe("days", 3) == "3 araw"
        assert self.locale._format_timeframe("days", 21) == "21 araw"

        # Weeks
        assert self.locale._format_timeframe("weeks", 0) == "0 linggo"
        assert self.locale._format_timeframe("weeks", 1) == "1 linggo"
        assert self.locale._format_timeframe("weeks", 2) == "2 linggo"
        assert self.locale._format_timeframe("weeks", 4) == "4 linggo"
        assert self.locale._format_timeframe("weeks", 5) == "5 linggo"
        assert self.locale._format_timeframe("weeks", 21) == "21 linggo"
        assert self.locale._format_timeframe("weeks", 22) == "22 linggo"
        assert self.locale._format_timeframe("weeks", 25) == "25 linggo"

        # Months
        assert self.locale._format_timeframe("months", 0) == "0 buwan"
        assert self.locale._format_timeframe("months", 1) == "1 buwan"
        assert self.locale._format_timeframe("months", 2) == "2 buwan"
        assert self.locale._format_timeframe("months", 4) == "4 buwan"
        assert self.locale._format_timeframe("months", 5) == "5 buwan"
        assert self.locale._format_timeframe("months", 21) == "21 buwan"
        assert self.locale._format_timeframe("months", 22) == "22 buwan"
        assert self.locale._format_timeframe("months", 25) == "25 buwan"

        # Years
        assert self.locale._format_timeframe("years", 1) == "1 taon"
        assert self.locale._format_timeframe("years", 2) == "2 taon"
        assert self.locale._format_timeframe("years", 5) == "5 taon"

    def test_multi_describe_tl(self):
        describe = self.locale.describe_multi

        fulltest = [("years", 5), ("weeks", 1), ("hours", 1), ("minutes", 6)]
        assert describe(fulltest) == "5 taon 1 linggo 1 oras 6 minuto mula ngayon"
        seconds4000_0days = [("days", 0), ("hours", 1), ("minutes", 6)]
        assert describe(seconds4000_0days) == "0 araw 1 oras 6 minuto mula ngayon"
        seconds4000 = [("hours", 1), ("minutes", 6)]
        assert describe(seconds4000) == "1 oras 6 minuto mula ngayon"
        assert describe(seconds4000, only_distance=True) == "1 oras 6 minuto"
        seconds3700 = [("hours", 1), ("minutes", 1)]
        assert describe(seconds3700) == "1 oras 1 minuto mula ngayon"
        seconds300_0hours = [("hours", 0), ("minutes", 5)]
        assert describe(seconds300_0hours) == "0 oras 5 minuto mula ngayon"
        seconds300 = [("minutes", 5)]
        assert describe(seconds300) == "5 minuto mula ngayon"
        seconds60 = [("minutes", 1)]
        assert describe(seconds60) == "1 minuto mula ngayon"
        assert describe(seconds60, only_distance=True) == "1 minuto"
        seconds60 = [("seconds", 1)]
        assert describe(seconds60) == "1 segundo mula ngayon"
        assert describe(seconds60, only_distance=True) == "1 segundo"

    def test_ordinal_number_tl(self):
        assert self.locale.ordinal_number(0) == "ika-0"
        assert self.locale.ordinal_number(1) == "ika-1"
        assert self.locale.ordinal_number(2) == "ika-2"
        assert self.locale.ordinal_number(3) == "ika-3"
        assert self.locale.ordinal_number(10) == "ika-10"
        assert self.locale.ordinal_number(23) == "ika-23"
        assert self.locale.ordinal_number(100) == "ika-100"
        assert self.locale.ordinal_number(103) == "ika-103"
        assert self.locale.ordinal_number(114) == "ika-114"


@pytest.mark.usefixtures("lang_locale")
class TestCroatianLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "upravo sad"
        assert self.locale._format_timeframe("second", 1) == "sekundu"
        assert self.locale._format_timeframe("seconds", 3) == "3 sekunde"
        assert self.locale._format_timeframe("seconds", 30) == "30 sekundi"
        assert self.locale._format_timeframe("minute", 1) == "minutu"
        assert self.locale._format_timeframe("minutes", 4) == "4 minute"
        assert self.locale._format_timeframe("minutes", 40) == "40 minuta"
        assert self.locale._format_timeframe("hour", 1) == "sat"
        assert self.locale._format_timeframe("hours", 23) == "23 sati"
        assert self.locale._format_timeframe("day", 1) == "jedan dan"
        assert self.locale._format_timeframe("days", 12) == "12 dana"
        assert self.locale._format_timeframe("month", 1) == "mjesec"
        assert self.locale._format_timeframe("months", 2) == "2 mjeseca"
        assert self.locale._format_timeframe("months", 11) == "11 mjeseci"
        assert self.locale._format_timeframe("year", 1) == "godinu"
        assert self.locale._format_timeframe("years", 2) == "2 godine"
        assert self.locale._format_timeframe("years", 12) == "12 godina"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "subota"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "su"


@pytest.mark.usefixtures("lang_locale")
class TestSerbianLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "sada"
        assert self.locale._format_timeframe("second", 1) == "sekundu"
        assert self.locale._format_timeframe("seconds", 3) == "3 sekunde"
        assert self.locale._format_timeframe("seconds", 30) == "30 sekundi"
        assert self.locale._format_timeframe("minute", 1) == "minutu"
        assert self.locale._format_timeframe("minutes", 4) == "4 minute"
        assert self.locale._format_timeframe("minutes", 40) == "40 minuta"
        assert self.locale._format_timeframe("hour", 1) == "sat"
        assert self.locale._format_timeframe("hours", 3) == "3 sata"
        assert self.locale._format_timeframe("hours", 23) == "23 sati"
        assert self.locale._format_timeframe("day", 1) == "dan"
        assert self.locale._format_timeframe("days", 12) == "12 dana"
        assert self.locale._format_timeframe("week", 1) == "nedelju"
        assert self.locale._format_timeframe("weeks", 2) == "2 nedelje"
        assert self.locale._format_timeframe("weeks", 11) == "11 nedelja"
        assert self.locale._format_timeframe("month", 1) == "mesec"
        assert self.locale._format_timeframe("months", 2) == "2 meseca"
        assert self.locale._format_timeframe("months", 11) == "11 meseci"
        assert self.locale._format_timeframe("year", 1) == "godinu"
        assert self.locale._format_timeframe("years", 2) == "2 godine"
        assert self.locale._format_timeframe("years", 12) == "12 godina"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "subota"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "su"


@pytest.mark.usefixtures("lang_locale")
class TestLatinLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "nunc"
        assert self.locale._format_timeframe("second", 1) == "secundum"
        assert self.locale._format_timeframe("seconds", 3) == "3 secundis"
        assert self.locale._format_timeframe("minute", 1) == "minutam"
        assert self.locale._format_timeframe("minutes", 4) == "4 minutis"
        assert self.locale._format_timeframe("hour", 1) == "horam"
        assert self.locale._format_timeframe("hours", 23) == "23 horas"
        assert self.locale._format_timeframe("day", 1) == "diem"
        assert self.locale._format_timeframe("days", 12) == "12 dies"
        assert self.locale._format_timeframe("month", 1) == "mensem"
        assert self.locale._format_timeframe("months", 11) == "11 mensis"
        assert self.locale._format_timeframe("year", 1) == "annum"
        assert self.locale._format_timeframe("years", 2) == "2 annos"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "dies Saturni"


@pytest.mark.usefixtures("lang_locale")
class TestLithuanianLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "dabar"
        assert self.locale._format_timeframe("second", 1) == "sekund??s"
        assert self.locale._format_timeframe("seconds", 3) == "3 sekund??i??"
        assert self.locale._format_timeframe("seconds", 30) == "30 sekund??i??"
        assert self.locale._format_timeframe("minute", 1) == "minut??s"
        assert self.locale._format_timeframe("minutes", 4) == "4 minu??i??"
        assert self.locale._format_timeframe("minutes", 40) == "40 minu??i??"
        assert self.locale._format_timeframe("hour", 1) == "valandos"
        assert self.locale._format_timeframe("hours", 23) == "23 valand??"
        assert self.locale._format_timeframe("day", 1) == "dien??"
        assert self.locale._format_timeframe("days", 12) == "12 dien??"
        assert self.locale._format_timeframe("month", 1) == "m??nesio"
        assert self.locale._format_timeframe("months", 2) == "2 m??nesi??"
        assert self.locale._format_timeframe("months", 11) == "11 m??nesi??"
        assert self.locale._format_timeframe("year", 1) == "met??"
        assert self.locale._format_timeframe("years", 2) == "2 met??"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "??e??tadienis"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "??e"


@pytest.mark.usefixtures("lang_locale")
class TestMalayLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "sekarang"
        assert self.locale._format_timeframe("second", 1) == "saat"
        assert self.locale._format_timeframe("seconds", 3) == "3 saat"
        assert self.locale._format_timeframe("minute", 1) == "minit"
        assert self.locale._format_timeframe("minutes", 4) == "4 minit"
        assert self.locale._format_timeframe("hour", 1) == "jam"
        assert self.locale._format_timeframe("hours", 23) == "23 jam"
        assert self.locale._format_timeframe("day", 1) == "hari"
        assert self.locale._format_timeframe("days", 12) == "12 hari"
        assert self.locale._format_timeframe("month", 1) == "bulan"
        assert self.locale._format_timeframe("months", 2) == "2 bulan"
        assert self.locale._format_timeframe("year", 1) == "tahun"
        assert self.locale._format_timeframe("years", 2) == "2 tahun"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "Sabtu"


@pytest.mark.usefixtures("lang_locale")
class TestSamiLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "d??l"
        assert self.locale._format_timeframe("second", 1) == "sekunda"
        assert self.locale._format_timeframe("seconds", 3) == "3 sekundda"
        assert self.locale._format_timeframe("minute", 1) == "minuhta"
        assert self.locale._format_timeframe("minutes", 4) == "4 minuhta"
        assert self.locale._format_timeframe("hour", 1) == "diimmu"
        assert self.locale._format_timeframe("hours", 23) == "23 diimmu"
        assert self.locale._format_timeframe("day", 1) == "beaivvi"
        assert self.locale._format_timeframe("days", 12) == "12 beaivvi"
        assert self.locale._format_timeframe("month", 1) == "m??nu"
        assert self.locale._format_timeframe("months", 2) == "2 m??nu"
        assert self.locale._format_timeframe("year", 1) == "jagi"
        assert self.locale._format_timeframe("years", 2) == "2 jagi"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "L??vvordat"


@pytest.mark.usefixtures("lang_locale")
class TestZuluLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "manje"
        assert self.locale._format_timeframe("second", -1) == "umzuzwana"
        assert self.locale._format_timeframe("second", 1) == "ngomzuzwana"
        assert self.locale._format_timeframe("seconds", -3) == "3 imizuzwana"
        assert self.locale._format_timeframe("minute", -1) == "umzuzu"
        assert self.locale._format_timeframe("minutes", -4) == "4 imizuzu"
        assert self.locale._format_timeframe("hour", -1) == "ihora"
        assert self.locale._format_timeframe("hours", -23) == "23 amahora"
        assert self.locale._format_timeframe("day", -1) == "usuku"
        assert self.locale._format_timeframe("days", -12) == "12 izinsuku"
        assert self.locale._format_timeframe("month", -1) == "inyanga"
        assert self.locale._format_timeframe("months", -2) == "2 izinyanga"
        assert self.locale._format_timeframe("year", -1) == "unyaka"
        assert self.locale._format_timeframe("years", -2) == "2 iminyaka"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "uMgqibelo"


@pytest.mark.usefixtures("lang_locale")
class TestAlbanianLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "tani"
        assert self.locale._format_timeframe("second", -1) == "sekond??"
        assert self.locale._format_timeframe("second", 1) == "sekond??"
        assert self.locale._format_timeframe("seconds", -3) == "3 sekonda"
        assert self.locale._format_timeframe("minute", 1) == "minut??"
        assert self.locale._format_timeframe("minutes", -4) == "4 minuta"
        assert self.locale._format_timeframe("hour", 1) == "or??"
        assert self.locale._format_timeframe("hours", -23) == "23 or??"
        assert self.locale._format_timeframe("day", 1) == "dit??"
        assert self.locale._format_timeframe("days", -12) == "12 dit??"
        assert self.locale._format_timeframe("week", 1) == "jav??"
        assert self.locale._format_timeframe("weeks", -12) == "12 jav??"
        assert self.locale._format_timeframe("month", 1) == "muaj"
        assert self.locale._format_timeframe("months", -2) == "2 muaj"
        assert self.locale._format_timeframe("year", 1) == "vit"
        assert self.locale._format_timeframe("years", -2) == "2 vjet"

    def test_weekday_and_month(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        # Saturday
        assert self.locale.day_name(dt.isoweekday()) == "e shtun??"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "sht"
        # June
        assert self.locale.month_name(dt.isoweekday()) == "qershor"
        assert self.locale.month_abbreviation(dt.isoweekday()) == "qer"


@pytest.mark.usefixtures("lang_locale")
class TestUrduLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "????????"
        assert self.locale._format_timeframe("second", -1) == "?????? ??????????"
        assert self.locale._format_timeframe("second", 1) == "?????? ??????????"
        assert self.locale._format_timeframe("seconds", -3) == "3 ??????????"
        assert self.locale._format_timeframe("minute", 1) == "?????? ??????"
        assert self.locale._format_timeframe("minutes", -4) == "4 ??????"
        assert self.locale._format_timeframe("hour", 1) == "?????? ??????????"
        assert self.locale._format_timeframe("hours", -23) == "23 ??????????"
        assert self.locale._format_timeframe("day", 1) == "?????? ????"
        assert self.locale._format_timeframe("days", -12) == "12 ????"
        assert self.locale._format_timeframe("week", 1) == "?????? ????????"
        assert self.locale._format_timeframe("weeks", -12) == "12 ????????"
        assert self.locale._format_timeframe("month", 1) == "?????? ??????????"
        assert self.locale._format_timeframe("months", -2) == "2 ??????"
        assert self.locale._format_timeframe("year", 1) == "?????? ??????"
        assert self.locale._format_timeframe("years", -2) == "2 ??????"

    def test_weekday_and_month(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        # Saturday
        assert self.locale.day_name(dt.isoweekday()) == "????????"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "????????"
        # June
        assert self.locale.month_name(dt.isoweekday()) == "??????"
        assert self.locale.month_abbreviation(dt.isoweekday()) == "??????"


@pytest.mark.usefixtures("lang_locale")
class TestEstonianLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "just n????d"
        assert self.locale._format_timeframe("second", 1) == "??he sekundi"
        assert self.locale._format_timeframe("seconds", 3) == "3 sekundi"
        assert self.locale._format_timeframe("seconds", 30) == "30 sekundi"
        assert self.locale._format_timeframe("minute", 1) == "??he minuti"
        assert self.locale._format_timeframe("minutes", 4) == "4 minuti"
        assert self.locale._format_timeframe("minutes", 40) == "40 minuti"
        assert self.locale._format_timeframe("hour", 1) == "tunni aja"
        assert self.locale._format_timeframe("hours", 5) == "5 tunni"
        assert self.locale._format_timeframe("hours", 23) == "23 tunni"
        assert self.locale._format_timeframe("day", 1) == "??he p??eva"
        assert self.locale._format_timeframe("days", 6) == "6 p??eva"
        assert self.locale._format_timeframe("days", 12) == "12 p??eva"
        assert self.locale._format_timeframe("month", 1) == "??he kuu"
        assert self.locale._format_timeframe("months", 7) == "7 kuu"
        assert self.locale._format_timeframe("months", 11) == "11 kuu"
        assert self.locale._format_timeframe("year", 1) == "??he aasta"
        assert self.locale._format_timeframe("years", 8) == "8 aasta"
        assert self.locale._format_timeframe("years", 12) == "12 aasta"

        assert self.locale._format_timeframe("now", 0) == "just n????d"
        assert self.locale._format_timeframe("second", -1) == "??ks sekund"
        assert self.locale._format_timeframe("seconds", -9) == "9 sekundit"
        assert self.locale._format_timeframe("seconds", -12) == "12 sekundit"
        assert self.locale._format_timeframe("minute", -1) == "??ks minut"
        assert self.locale._format_timeframe("minutes", -2) == "2 minutit"
        assert self.locale._format_timeframe("minutes", -10) == "10 minutit"
        assert self.locale._format_timeframe("hour", -1) == "tund aega"
        assert self.locale._format_timeframe("hours", -3) == "3 tundi"
        assert self.locale._format_timeframe("hours", -11) == "11 tundi"
        assert self.locale._format_timeframe("day", -1) == "??ks p??ev"
        assert self.locale._format_timeframe("days", -2) == "2 p??eva"
        assert self.locale._format_timeframe("days", -12) == "12 p??eva"
        assert self.locale._format_timeframe("month", -1) == "??ks kuu"
        assert self.locale._format_timeframe("months", -3) == "3 kuud"
        assert self.locale._format_timeframe("months", -13) == "13 kuud"
        assert self.locale._format_timeframe("year", -1) == "??ks aasta"
        assert self.locale._format_timeframe("years", -4) == "4 aastat"
        assert self.locale._format_timeframe("years", -14) == "14 aastat"


@pytest.mark.usefixtures("lang_locale")
class TestPortugueseLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "agora"
        assert self.locale._format_timeframe("second", 1) == "um segundo"
        assert self.locale._format_timeframe("seconds", 30) == "30 segundos"
        assert self.locale._format_timeframe("minute", 1) == "um minuto"
        assert self.locale._format_timeframe("minutes", 40) == "40 minutos"
        assert self.locale._format_timeframe("hour", 1) == "uma hora"
        assert self.locale._format_timeframe("hours", 23) == "23 horas"
        assert self.locale._format_timeframe("day", 1) == "um dia"
        assert self.locale._format_timeframe("days", 12) == "12 dias"
        assert self.locale._format_timeframe("month", 1) == "um m??s"
        assert self.locale._format_timeframe("months", 11) == "11 meses"
        assert self.locale._format_timeframe("year", 1) == "um ano"
        assert self.locale._format_timeframe("years", 12) == "12 anos"


@pytest.mark.usefixtures("lang_locale")
class TestLatvianLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "tagad"
        assert self.locale._format_timeframe("second", 1) == "sekundes"
        assert self.locale._format_timeframe("seconds", 3) == "3 sekund??m"
        assert self.locale._format_timeframe("seconds", 30) == "30 sekund??m"
        assert self.locale._format_timeframe("minute", 1) == "min??tes"
        assert self.locale._format_timeframe("minutes", 4) == "4 min??t??m"
        assert self.locale._format_timeframe("minutes", 40) == "40 min??t??m"
        assert self.locale._format_timeframe("hour", 1) == "stundas"
        assert self.locale._format_timeframe("hours", 23) == "23 stund??m"
        assert self.locale._format_timeframe("day", 1) == "dienas"
        assert self.locale._format_timeframe("days", 12) == "12 dien??m"
        assert self.locale._format_timeframe("month", 1) == "m??ne??a"
        assert self.locale._format_timeframe("months", 2) == "2 m??ne??iem"
        assert self.locale._format_timeframe("months", 11) == "11 m??ne??iem"
        assert self.locale._format_timeframe("year", 1) == "gada"
        assert self.locale._format_timeframe("years", 2) == "2 gadiem"
        assert self.locale._format_timeframe("years", 12) == "12 gadiem"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "sestdiena"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "se"


@pytest.mark.usefixtures("lang_locale")
class TestBrazilianPortugueseLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "agora"
        assert self.locale._format_timeframe("second", 1) == "um segundo"
        assert self.locale._format_timeframe("seconds", 30) == "30 segundos"
        assert self.locale._format_timeframe("minute", 1) == "um minuto"
        assert self.locale._format_timeframe("minutes", 40) == "40 minutos"
        assert self.locale._format_timeframe("hour", 1) == "uma hora"
        assert self.locale._format_timeframe("hours", 23) == "23 horas"
        assert self.locale._format_timeframe("day", 1) == "um dia"
        assert self.locale._format_timeframe("days", 12) == "12 dias"
        assert self.locale._format_timeframe("month", 1) == "um m??s"
        assert self.locale._format_timeframe("months", 11) == "11 meses"
        assert self.locale._format_timeframe("year", 1) == "um ano"
        assert self.locale._format_timeframe("years", 12) == "12 anos"
        assert self.locale._format_relative("uma hora", "hour", -1) == "faz uma hora"


@pytest.mark.usefixtures("lang_locale")
class TestHongKongLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "??????"
        assert self.locale._format_timeframe("second", 1) == "1???"
        assert self.locale._format_timeframe("seconds", 30) == "30???"
        assert self.locale._format_timeframe("minute", 1) == "1??????"
        assert self.locale._format_timeframe("minutes", 40) == "40??????"
        assert self.locale._format_timeframe("hour", 1) == "1??????"
        assert self.locale._format_timeframe("hours", 23) == "23??????"
        assert self.locale._format_timeframe("day", 1) == "1???"
        assert self.locale._format_timeframe("days", 12) == "12???"
        assert self.locale._format_timeframe("week", 1) == "1??????"
        assert self.locale._format_timeframe("weeks", 38) == "38??????"
        assert self.locale._format_timeframe("month", 1) == "1??????"
        assert self.locale._format_timeframe("months", 11) == "11??????"
        assert self.locale._format_timeframe("year", 1) == "1???"
        assert self.locale._format_timeframe("years", 12) == "12???"


@pytest.mark.usefixtures("lang_locale")
class TestChineseTWLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "??????"
        assert self.locale._format_timeframe("second", 1) == "1???"
        assert self.locale._format_timeframe("seconds", 30) == "30???"
        assert self.locale._format_timeframe("minute", 1) == "1??????"
        assert self.locale._format_timeframe("minutes", 40) == "40??????"
        assert self.locale._format_timeframe("hour", 1) == "1??????"
        assert self.locale._format_timeframe("hours", 23) == "23??????"
        assert self.locale._format_timeframe("day", 1) == "1???"
        assert self.locale._format_timeframe("days", 12) == "12???"
        assert self.locale._format_timeframe("week", 1) == "1???"
        assert self.locale._format_timeframe("weeks", 38) == "38???"
        assert self.locale._format_timeframe("month", 1) == "1??????"
        assert self.locale._format_timeframe("months", 11) == "11??????"
        assert self.locale._format_timeframe("year", 1) == "1???"
        assert self.locale._format_timeframe("years", 12) == "12???"


@pytest.mark.usefixtures("lang_locale")
class TestChineseCNLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "??????"
        assert self.locale._format_timeframe("second", 1) == "??????"
        assert self.locale._format_timeframe("seconds", 30) == "30???"
        assert self.locale._format_timeframe("minute", 1) == "1??????"
        assert self.locale._format_timeframe("minutes", 40) == "40??????"
        assert self.locale._format_timeframe("hour", 1) == "1??????"
        assert self.locale._format_timeframe("hours", 23) == "23??????"
        assert self.locale._format_timeframe("day", 1) == "1???"
        assert self.locale._format_timeframe("days", 12) == "12???"
        assert self.locale._format_timeframe("week", 1) == "??????"
        assert self.locale._format_timeframe("weeks", 38) == "38???"
        assert self.locale._format_timeframe("month", 1) == "1??????"
        assert self.locale._format_timeframe("months", 11) == "11??????"
        assert self.locale._format_timeframe("year", 1) == "1???"
        assert self.locale._format_timeframe("years", 12) == "12???"


@pytest.mark.usefixtures("lang_locale")
class TestSwahiliLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "sasa hivi"
        assert self.locale._format_timeframe("second", 1) == "sekunde"
        assert self.locale._format_timeframe("seconds", 3) == "sekunde 3"
        assert self.locale._format_timeframe("seconds", 30) == "sekunde 30"
        assert self.locale._format_timeframe("minute", 1) == "dakika moja"
        assert self.locale._format_timeframe("minutes", 4) == "dakika 4"
        assert self.locale._format_timeframe("minutes", 40) == "dakika 40"
        assert self.locale._format_timeframe("hour", 1) == "saa moja"
        assert self.locale._format_timeframe("hours", 5) == "saa 5"
        assert self.locale._format_timeframe("hours", 23) == "saa 23"
        assert self.locale._format_timeframe("day", 1) == "siku moja"
        assert self.locale._format_timeframe("days", 6) == "siku 6"
        assert self.locale._format_timeframe("days", 12) == "siku 12"
        assert self.locale._format_timeframe("month", 1) == "mwezi moja"
        assert self.locale._format_timeframe("months", 7) == "miezi 7"
        assert self.locale._format_timeframe("week", 1) == "wiki moja"
        assert self.locale._format_timeframe("weeks", 2) == "wiki 2"
        assert self.locale._format_timeframe("months", 11) == "miezi 11"
        assert self.locale._format_timeframe("year", 1) == "mwaka moja"
        assert self.locale._format_timeframe("years", 8) == "miaka 8"
        assert self.locale._format_timeframe("years", 12) == "miaka 12"

    def test_format_relative_now(self):
        result = self.locale._format_relative("sasa hivi", "now", 0)
        assert result == "sasa hivi"

    def test_format_relative_past(self):
        result = self.locale._format_relative("saa moja", "hour", 1)
        assert result == "muda wa saa moja"

    def test_format_relative_future(self):
        result = self.locale._format_relative("saa moja", "hour", -1)
        assert result == "saa moja iliyopita"


@pytest.mark.usefixtures("lang_locale")
class TestKoreanLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "??????"
        assert self.locale._format_timeframe("second", 1) == "1???"
        assert self.locale._format_timeframe("seconds", 2) == "2???"
        assert self.locale._format_timeframe("minute", 1) == "1???"
        assert self.locale._format_timeframe("minutes", 2) == "2???"
        assert self.locale._format_timeframe("hour", 1) == "?????????"
        assert self.locale._format_timeframe("hours", 2) == "2??????"
        assert self.locale._format_timeframe("day", 1) == "??????"
        assert self.locale._format_timeframe("days", 2) == "2???"
        assert self.locale._format_timeframe("week", 1) == "1???"
        assert self.locale._format_timeframe("weeks", 2) == "2???"
        assert self.locale._format_timeframe("month", 1) == "??????"
        assert self.locale._format_timeframe("months", 2) == "2??????"
        assert self.locale._format_timeframe("year", 1) == "1???"
        assert self.locale._format_timeframe("years", 2) == "2???"

    def test_format_relative(self):
        assert self.locale._format_relative("??????", "now", 0) == "??????"

        assert self.locale._format_relative("1???", "second", 1) == "1??? ???"
        assert self.locale._format_relative("2???", "seconds", 2) == "2??? ???"
        assert self.locale._format_relative("1???", "minute", 1) == "1??? ???"
        assert self.locale._format_relative("2???", "minutes", 2) == "2??? ???"
        assert self.locale._format_relative("?????????", "hour", 1) == "????????? ???"
        assert self.locale._format_relative("2??????", "hours", 2) == "2?????? ???"
        assert self.locale._format_relative("??????", "day", 1) == "??????"
        assert self.locale._format_relative("2???", "days", 2) == "??????"
        assert self.locale._format_relative("3???", "days", 3) == "??????"
        assert self.locale._format_relative("4???", "days", 4) == "?????????"
        assert self.locale._format_relative("5???", "days", 5) == "5??? ???"
        assert self.locale._format_relative("1???", "week", 1) == "1??? ???"
        assert self.locale._format_relative("2???", "weeks", 2) == "2??? ???"
        assert self.locale._format_relative("??????", "month", 1) == "?????? ???"
        assert self.locale._format_relative("2??????", "months", 2) == "2?????? ???"
        assert self.locale._format_relative("1???", "year", 1) == "??????"
        assert self.locale._format_relative("2???", "years", 2) == "?????????"
        assert self.locale._format_relative("3???", "years", 3) == "3??? ???"

        assert self.locale._format_relative("1???", "second", -1) == "1??? ???"
        assert self.locale._format_relative("2???", "seconds", -2) == "2??? ???"
        assert self.locale._format_relative("1???", "minute", -1) == "1??? ???"
        assert self.locale._format_relative("2???", "minutes", -2) == "2??? ???"
        assert self.locale._format_relative("?????????", "hour", -1) == "????????? ???"
        assert self.locale._format_relative("2??????", "hours", -2) == "2?????? ???"
        assert self.locale._format_relative("??????", "day", -1) == "??????"
        assert self.locale._format_relative("2???", "days", -2) == "??????"
        assert self.locale._format_relative("3???", "days", -3) == "?????????"
        assert self.locale._format_relative("4???", "days", -4) == "4??? ???"
        assert self.locale._format_relative("1???", "week", -1) == "1??? ???"
        assert self.locale._format_relative("2???", "weeks", -2) == "2??? ???"
        assert self.locale._format_relative("??????", "month", -1) == "?????? ???"
        assert self.locale._format_relative("2??????", "months", -2) == "2?????? ???"
        assert self.locale._format_relative("1???", "year", -1) == "??????"
        assert self.locale._format_relative("2???", "years", -2) == "?????????"
        assert self.locale._format_relative("3???", "years", -3) == "3??? ???"

    def test_ordinal_number(self):
        assert self.locale.ordinal_number(0) == "0??????"
        assert self.locale.ordinal_number(1) == "?????????"
        assert self.locale.ordinal_number(2) == "?????????"
        assert self.locale.ordinal_number(3) == "?????????"
        assert self.locale.ordinal_number(4) == "?????????"
        assert self.locale.ordinal_number(5) == "????????????"
        assert self.locale.ordinal_number(6) == "????????????"
        assert self.locale.ordinal_number(7) == "????????????"
        assert self.locale.ordinal_number(8) == "????????????"
        assert self.locale.ordinal_number(9) == "????????????"
        assert self.locale.ordinal_number(10) == "?????????"
        assert self.locale.ordinal_number(11) == "11??????"
        assert self.locale.ordinal_number(12) == "12??????"
        assert self.locale.ordinal_number(100) == "100??????"


@pytest.mark.usefixtures("lang_locale")
class TestJapaneseLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "??????"
        assert self.locale._format_timeframe("second", 1) == "1???"
        assert self.locale._format_timeframe("seconds", 30) == "30???"
        assert self.locale._format_timeframe("minute", 1) == "1???"
        assert self.locale._format_timeframe("minutes", 40) == "40???"
        assert self.locale._format_timeframe("hour", 1) == "1??????"
        assert self.locale._format_timeframe("hours", 23) == "23??????"
        assert self.locale._format_timeframe("day", 1) == "1???"
        assert self.locale._format_timeframe("days", 12) == "12???"
        assert self.locale._format_timeframe("week", 1) == "1??????"
        assert self.locale._format_timeframe("weeks", 38) == "38??????"
        assert self.locale._format_timeframe("month", 1) == "1??????"
        assert self.locale._format_timeframe("months", 11) == "11??????"
        assert self.locale._format_timeframe("year", 1) == "1???"
        assert self.locale._format_timeframe("years", 12) == "12???"


@pytest.mark.usefixtures("lang_locale")
class TestSwedishLocale:
    def test_plurals(self):
        assert self.locale._format_timeframe("now", 0) == "just nu"
        assert self.locale._format_timeframe("second", 1) == "en sekund"
        assert self.locale._format_timeframe("seconds", 30) == "30 sekunder"
        assert self.locale._format_timeframe("minute", 1) == "en minut"
        assert self.locale._format_timeframe("minutes", 40) == "40 minuter"
        assert self.locale._format_timeframe("hour", 1) == "en timme"
        assert self.locale._format_timeframe("hours", 23) == "23 timmar"
        assert self.locale._format_timeframe("day", 1) == "en dag"
        assert self.locale._format_timeframe("days", 12) == "12 dagar"
        assert self.locale._format_timeframe("week", 1) == "en vecka"
        assert self.locale._format_timeframe("weeks", 38) == "38 veckor"
        assert self.locale._format_timeframe("month", 1) == "en m??nad"
        assert self.locale._format_timeframe("months", 11) == "11 m??nader"
        assert self.locale._format_timeframe("year", 1) == "ett ??r"
        assert self.locale._format_timeframe("years", 12) == "12 ??r"


@pytest.mark.usefixtures("lang_locale")
class TestOdiaLocale:
    def test_ordinal_number(self):
        assert self.locale._ordinal_number(0) == "0??????"
        assert self.locale._ordinal_number(1) == "1???"
        assert self.locale._ordinal_number(3) == "3???"
        assert self.locale._ordinal_number(4) == "4?????????"
        assert self.locale._ordinal_number(5) == "5???"
        assert self.locale._ordinal_number(6) == "6?????????"
        assert self.locale._ordinal_number(10) == "10???"
        assert self.locale._ordinal_number(11) == "11??????"
        assert self.locale._ordinal_number(42) == "42??????"
        assert self.locale._ordinal_number(-1) == ""

    def test_format_timeframe(self):

        assert self.locale._format_timeframe("hours", 2) == "2 ???????????????"
        assert self.locale._format_timeframe("hour", 0) == "?????? ???????????????"

    def test_format_relative_now(self):

        result = self.locale._format_relative("???????????????????????????", "now", 0)
        assert result == "???????????????????????????"

    def test_format_relative_past(self):

        result = self.locale._format_relative("?????? ???????????????", "hour", 1)
        assert result == "?????? ??????????????? ?????????"

    def test_format_relative_future(self):

        result = self.locale._format_relative("?????? ???????????????", "hour", -1)
        assert result == "?????? ??????????????? ??????????????????"


@pytest.mark.usefixtures("lang_locale")
class TestTurkishLocale:
    def test_singles_mk(self):
        assert self.locale._format_timeframe("second", 1) == "bir saniye"
        assert self.locale._format_timeframe("minute", 1) == "bir dakika"
        assert self.locale._format_timeframe("hour", 1) == "bir saat"
        assert self.locale._format_timeframe("day", 1) == "bir g??n"
        assert self.locale._format_timeframe("week", 1) == "bir hafta"
        assert self.locale._format_timeframe("month", 1) == "bir ay"
        assert self.locale._format_timeframe("year", 1) == "bir y??l"

    def test_meridians_mk(self):
        assert self.locale.meridian(7, "A") == "????"
        assert self.locale.meridian(18, "A") == "??S"
        assert self.locale.meridian(10, "a") == "????"
        assert self.locale.meridian(22, "a") == "??s"

    def test_describe_mk(self):
        assert self.locale.describe("second", only_distance=True) == "bir saniye"
        assert self.locale.describe("second", only_distance=False) == "bir saniye sonra"
        assert self.locale.describe("minute", only_distance=True) == "bir dakika"
        assert self.locale.describe("minute", only_distance=False) == "bir dakika sonra"
        assert self.locale.describe("hour", only_distance=True) == "bir saat"
        assert self.locale.describe("hour", only_distance=False) == "bir saat sonra"
        assert self.locale.describe("day", only_distance=True) == "bir g??n"
        assert self.locale.describe("day", only_distance=False) == "bir g??n sonra"
        assert self.locale.describe("week", only_distance=True) == "bir hafta"
        assert self.locale.describe("week", only_distance=False) == "bir hafta sonra"
        assert self.locale.describe("month", only_distance=True) == "bir ay"
        assert self.locale.describe("month", only_distance=False) == "bir ay sonra"
        assert self.locale.describe("year", only_distance=True) == "bir y??l"
        assert self.locale.describe("year", only_distance=False) == "bir y??l sonra"

    def test_relative_mk(self):
        assert self.locale._format_relative("??imdi", "now", 0) == "??imdi"
        assert (
            self.locale._format_relative("1 saniye", "seconds", 1) == "1 saniye sonra"
        )
        assert (
            self.locale._format_relative("1 saniye", "seconds", -1) == "1 saniye ??nce"
        )
        assert (
            self.locale._format_relative("1 dakika", "minutes", 1) == "1 dakika sonra"
        )
        assert (
            self.locale._format_relative("1 dakika", "minutes", -1) == "1 dakika ??nce"
        )
        assert self.locale._format_relative("1 saat", "hours", 1) == "1 saat sonra"
        assert self.locale._format_relative("1 saat", "hours", -1) == "1 saat ??nce"
        assert self.locale._format_relative("1 g??n", "days", 1) == "1 g??n sonra"
        assert self.locale._format_relative("1 g??n", "days", -1) == "1 g??n ??nce"
        assert self.locale._format_relative("1 hafta", "weeks", 1) == "1 hafta sonra"
        assert self.locale._format_relative("1 hafta", "weeks", -1) == "1 hafta ??nce"
        assert self.locale._format_relative("1 ay", "months", 1) == "1 ay sonra"
        assert self.locale._format_relative("1 ay", "months", -1) == "1 ay ??nce"
        assert self.locale._format_relative("1 y??l", "years", 1) == "1 y??l sonra"
        assert self.locale._format_relative("1 y??l", "years", -1) == "1 y??l ??nce"

    def test_plurals_mk(self):
        assert self.locale._format_timeframe("now", 0) == "??imdi"
        assert self.locale._format_timeframe("second", 1) == "bir saniye"
        assert self.locale._format_timeframe("seconds", 30) == "30 saniye"
        assert self.locale._format_timeframe("minute", 1) == "bir dakika"
        assert self.locale._format_timeframe("minutes", 40) == "40 dakika"
        assert self.locale._format_timeframe("hour", 1) == "bir saat"
        assert self.locale._format_timeframe("hours", 23) == "23 saat"
        assert self.locale._format_timeframe("day", 1) == "bir g??n"
        assert self.locale._format_timeframe("days", 12) == "12 g??n"
        assert self.locale._format_timeframe("week", 1) == "bir hafta"
        assert self.locale._format_timeframe("weeks", 38) == "38 hafta"
        assert self.locale._format_timeframe("month", 1) == "bir ay"
        assert self.locale._format_timeframe("months", 11) == "11 ay"
        assert self.locale._format_timeframe("year", 1) == "bir y??l"
        assert self.locale._format_timeframe("years", 12) == "12 y??l"


@pytest.mark.usefixtures("lang_locale")
class TestLuxembourgishLocale:
    def test_ordinal_number(self):
        assert self.locale.ordinal_number(1) == "1."

    def test_define(self):
        assert self.locale.describe("minute", only_distance=True) == "eng Minutt"
        assert self.locale.describe("minute", only_distance=False) == "an enger Minutt"
        assert self.locale.describe("hour", only_distance=True) == "eng Stonn"
        assert self.locale.describe("hour", only_distance=False) == "an enger Stonn"
        assert self.locale.describe("day", only_distance=True) == "een Dag"
        assert self.locale.describe("day", only_distance=False) == "an engem Dag"
        assert self.locale.describe("week", only_distance=True) == "eng Woch"
        assert self.locale.describe("week", only_distance=False) == "an enger Woch"
        assert self.locale.describe("month", only_distance=True) == "ee Mount"
        assert self.locale.describe("month", only_distance=False) == "an engem Mount"
        assert self.locale.describe("year", only_distance=True) == "ee Joer"
        assert self.locale.describe("year", only_distance=False) == "an engem Joer"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "Samschdeg"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "Sam"


@pytest.mark.usefixtures("lang_locale")
class TestTamilLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "?????????????????????"
        assert self.locale._format_timeframe("second", 1) == "????????? ???????????????????????????"
        assert self.locale._format_timeframe("seconds", 3) == "3 ???????????????????????????"
        assert self.locale._format_timeframe("minute", 1) == "????????? ?????????????????????"
        assert self.locale._format_timeframe("minutes", 4) == "4 ??????????????????????????????"
        assert self.locale._format_timeframe("hour", 1) == "????????? ?????????"
        assert self.locale._format_timeframe("hours", 23) == "23 ????????????????????????"
        assert self.locale._format_timeframe("day", 1) == "????????? ????????????"
        assert self.locale._format_timeframe("days", 12) == "12 ?????????????????????"
        assert self.locale._format_timeframe("week", 1) == "????????? ???????????????"
        assert self.locale._format_timeframe("weeks", 12) == "12 ????????????????????????"
        assert self.locale._format_timeframe("month", 1) == "????????? ???????????????"
        assert self.locale._format_timeframe("months", 2) == "2 ????????????????????????"
        assert self.locale._format_timeframe("year", 1) == "????????? ???????????????"
        assert self.locale._format_timeframe("years", 2) == "2 ????????????????????????"

    def test_ordinal_number(self):
        assert self.locale._ordinal_number(0) == "0?????????"
        assert self.locale._ordinal_number(1) == "1?????????"
        assert self.locale._ordinal_number(3) == "3?????????"
        assert self.locale._ordinal_number(11) == "11?????????"
        assert self.locale._ordinal_number(-1) == ""

    def test_format_relative_now(self):
        result = self.locale._format_relative("?????????????????????", "now", 0)
        assert result == "?????????????????????"

    def test_format_relative_past(self):
        result = self.locale._format_relative("????????? ?????????", "hour", 1)
        assert result == "????????? ????????? ?????????"

    def test_format_relative_future(self):
        result = self.locale._format_relative("????????? ?????????", "hour", -1)
        assert result == "????????? ????????? ????????????????????????????????? ??????????????????"

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "??????????????????????????????"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "?????????"


@pytest.mark.usefixtures("lang_locale")
class TestSinhalaLocale:
    def test_format_timeframe(self):
        assert self.locale._format_timeframe("now", 0) == "????????????"
        assert self.locale._format_timeframe("second", -1) == "?????????????????????"
        assert self.locale._format_timeframe("second", 1) == "??????????????????????????????"
        assert self.locale._format_timeframe("seconds", -30) == "??????????????? 30 ???"

        assert self.locale._format_timeframe("minute", -1) == "????????????????????????"
        assert self.locale._format_timeframe("minutes", 4) == "???????????????????????? 4 ????????????"

        assert self.locale._format_timeframe("hour", -1) == "????????????"
        assert self.locale._format_timeframe("hours", 23) == "????????? 23 ????????????"

        assert self.locale._format_timeframe("day", 1) == "???????????????"
        assert self.locale._format_timeframe("days", -12) == "????????? 12 ???"

        assert self.locale._format_timeframe("week", -1) == "???????????????"
        assert self.locale._format_timeframe("weeks", -10) == "????????? 10 ???"

        assert self.locale._format_timeframe("month", -1) == "???????????????"
        assert self.locale._format_timeframe("months", -2) == "????????? 2 ???"

        assert self.locale._format_timeframe("year", 1) == "??????????????? ?????????"
        assert self.locale._format_timeframe("years", -21) == "????????????????????? 21 ???"

    def test_describe_si(self):
        assert self.locale.describe("second", only_distance=True) == "????????????????????????"
        assert (
            self.locale.describe("second", only_distance=False) == "??????????????????????????????"
        )  # (in) a second

        assert self.locale.describe("minute", only_distance=True) == "?????????????????????????????????"
        assert (
            self.locale.describe("minute", only_distance=False) == "?????????????????????????????????"
        )  # (in) a minute

        assert self.locale.describe("hour", only_distance=True) == "???????????????"
        assert self.locale.describe("hour", only_distance=False) == "?????????????????????"

        assert self.locale.describe("day", only_distance=True) == "???????????????"
        assert self.locale.describe("day", only_distance=False) == "???????????????"

        assert self.locale.describe("week", only_distance=True) == "??????????????????"
        assert self.locale.describe("week", only_distance=False) == "????????????????????????"

        assert self.locale.describe("month", only_distance=True) == "??????????????????"
        assert self.locale.describe("month", only_distance=False) == "?????? ???????????? ?????????"

        assert self.locale.describe("year", only_distance=True) == "??????????????????????????????"
        assert self.locale.describe("year", only_distance=False) == "??????????????? ?????????"

    def test_format_relative_now(self):
        result = self.locale._format_relative("????????????", "now", 0)
        assert result == "????????????"

    def test_format_relative_future(self):

        result = self.locale._format_relative("?????????????????????", "?????????", 1)

        assert result == "?????????????????????"  # (in) one hour

    def test_format_relative_past(self):

        result = self.locale._format_relative("????????????", "?????????", -1)

        assert result == "??????????????? ?????????"  # an hour ago

    def test_weekday(self):
        dt = arrow.Arrow(2015, 4, 11, 17, 30, 00)
        assert self.locale.day_name(dt.isoweekday()) == "???????????????????????????"
        assert self.locale.day_abbreviation(dt.isoweekday()) == "???"
