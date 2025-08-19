from __future__ import annotations

import re
from enum import Enum
from typing import ClassVar

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

__all__ = [
    "MySQLAccessAdd",
    "MySQLDbAdd",
    "MySQLPasswd",
    "MySQLPrivileges",
    "MySQLUserAdd",
]


class MySQLCollate(str, Enum):
    armscii8_bin = "armscii8_bin"
    armscii8_general_ci = "armscii8_general_ci"
    ascii_bin = "ascii_bin"
    ascii_general_ci = "ascii_general_ci"
    big5_bin = "big5_bin"
    big5_chinese_ci = "big5_chinese_ci"
    binary = "binary"
    cp1250_bin = "cp1250_bin"
    cp1250_croatian_ci = "cp1250_croatian_ci"
    cp1250_czech_cs = "cp1250_czech_cs"
    cp1250_general_ci = "cp1250_general_ci"
    cp1250_polish_ci = "cp1250_polish_ci"
    cp1251_bin = "cp1251_bin"
    cp1251_bulgarian_ci = "cp1251_bulgarian_ci"
    cp1251_general_ci = "cp1251_general_ci"
    cp1251_general_cs = "cp1251_general_cs"
    cp1251_ukrainian_ci = "cp1251_ukrainian_ci"
    cp1256_bin = "cp1256_bin"
    cp1256_general_ci = "cp1256_general_ci"
    cp1257_bin = "cp1257_bin"
    cp1257_general_ci = "cp1257_general_ci"
    cp1257_lithuanian_ci = "cp1257_lithuanian_ci"
    cp850_bin = "cp850_bin"
    cp850_general_ci = "cp850_general_ci"
    cp852_bin = "cp852_bin"
    cp852_general_ci = "cp852_general_ci"
    cp866_bin = "cp866_bin"
    cp866_general_ci = "cp866_general_ci"
    cp932_bin = "cp932_bin"
    cp932_japanese_ci = "cp932_japanese_ci"
    dec8_bin = "dec8_bin"
    dec8_swedish_ci = "dec8_swedish_ci"
    eucjpms_bin = "eucjpms_bin"
    eucjpms_japanese_ci = "eucjpms_japanese_ci"
    euckr_bin = "euckr_bin"
    euckr_korean_ci = "euckr_korean_ci"
    gb18030_bin = "gb18030_bin"
    gb18030_chinese_ci = "gb18030_chinese_ci"
    gb18030_unicode_520_ci = "gb18030_unicode_520_ci"
    gb2312_bin = "gb2312_bin"
    gb2312_chinese_ci = "gb2312_chinese_ci"
    gbk_bin = "gbk_bin"
    gbk_chinese_ci = "gbk_chinese_ci"
    geostd8_bin = "geostd8_bin"
    geostd8_general_ci = "geostd8_general_ci"
    greek_bin = "greek_bin"
    greek_general_ci = "greek_general_ci"
    hebrew_bin = "hebrew_bin"
    hebrew_general_ci = "hebrew_general_ci"
    hp8_bin = "hp8_bin"
    hp8_english_ci = "hp8_english_ci"
    keybcs2_bin = "keybcs2_bin"
    keybcs2_general_ci = "keybcs2_general_ci"
    koi8r_bin = "koi8r_bin"
    koi8r_general_ci = "koi8r_general_ci"
    koi8u_bin = "koi8u_bin"
    koi8u_general_ci = "koi8u_general_ci"
    latin1_bin = "latin1_bin"
    latin1_danish_ci = "latin1_danish_ci"
    latin1_general_ci = "latin1_general_ci"
    latin1_general_cs = "latin1_general_cs"
    latin1_german1_ci = "latin1_german1_ci"
    latin1_german2_ci = "latin1_german2_ci"
    latin1_spanish_ci = "latin1_spanish_ci"
    latin1_swedish_ci = "latin1_swedish_ci"
    latin2_bin = "latin2_bin"
    latin2_croatian_ci = "latin2_croatian_ci"
    latin2_czech_cs = "latin2_czech_cs"
    latin2_general_ci = "latin2_general_ci"
    latin2_hungarian_ci = "latin2_hungarian_ci"
    latin5_bin = "latin5_bin"
    latin5_turkish_ci = "latin5_turkish_ci"
    latin7_bin = "latin7_bin"
    latin7_estonian_cs = "latin7_estonian_cs"
    latin7_general_ci = "latin7_general_ci"
    latin7_general_cs = "latin7_general_cs"
    macce_bin = "macce_bin"
    macce_general_ci = "macce_general_ci"
    macroman_bin = "macroman_bin"
    macroman_general_ci = "macroman_general_ci"
    sjis_bin = "sjis_bin"
    sjis_japanese_ci = "sjis_japanese_ci"
    swe7_bin = "swe7_bin"
    swe7_swedish_ci = "swe7_swedish_ci"
    tis620_bin = "tis620_bin"
    tis620_thai_ci = "tis620_thai_ci"
    ucs2_bin = "ucs2_bin"
    ucs2_croatian_ci = "ucs2_croatian_ci"
    ucs2_czech_ci = "ucs2_czech_ci"
    ucs2_danish_ci = "ucs2_danish_ci"
    ucs2_esperanto_ci = "ucs2_esperanto_ci"
    ucs2_estonian_ci = "ucs2_estonian_ci"
    ucs2_general_ci = "ucs2_general_ci"
    ucs2_general_mysql500_ci = "ucs2_general_mysql500_ci"
    ucs2_german2_ci = "ucs2_german2_ci"
    ucs2_hungarian_ci = "ucs2_hungarian_ci"
    ucs2_icelandic_ci = "ucs2_icelandic_ci"
    ucs2_latvian_ci = "ucs2_latvian_ci"
    ucs2_lithuanian_ci = "ucs2_lithuanian_ci"
    ucs2_persian_ci = "ucs2_persian_ci"
    ucs2_polish_ci = "ucs2_polish_ci"
    ucs2_romanian_ci = "ucs2_romanian_ci"
    ucs2_roman_ci = "ucs2_roman_ci"
    ucs2_sinhala_ci = "ucs2_sinhala_ci"
    ucs2_slovak_ci = "ucs2_slovak_ci"
    ucs2_slovenian_ci = "ucs2_slovenian_ci"
    ucs2_spanish2_ci = "ucs2_spanish2_ci"
    ucs2_spanish_ci = "ucs2_spanish_ci"
    ucs2_swedish_ci = "ucs2_swedish_ci"
    ucs2_turkish_ci = "ucs2_turkish_ci"
    ucs2_unicode_520_ci = "ucs2_unicode_520_ci"
    ucs2_unicode_ci = "ucs2_unicode_ci"
    ucs2_vietnamese_ci = "ucs2_vietnamese_ci"
    ujis_bin = "ujis_bin"
    ujis_japanese_ci = "ujis_japanese_ci"
    utf16_bin = "utf16_bin"
    utf16_croatian_ci = "utf16_croatian_ci"
    utf16_czech_ci = "utf16_czech_ci"
    utf16_danish_ci = "utf16_danish_ci"
    utf16_esperanto_ci = "utf16_esperanto_ci"
    utf16_estonian_ci = "utf16_estonian_ci"
    utf16_general_ci = "utf16_general_ci"
    utf16_german2_ci = "utf16_german2_ci"
    utf16_hungarian_ci = "utf16_hungarian_ci"
    utf16_icelandic_ci = "utf16_icelandic_ci"
    utf16_latvian_ci = "utf16_latvian_ci"
    utf16_lithuanian_ci = "utf16_lithuanian_ci"
    utf16_persian_ci = "utf16_persian_ci"
    utf16_polish_ci = "utf16_polish_ci"
    utf16_romanian_ci = "utf16_romanian_ci"
    utf16_roman_ci = "utf16_roman_ci"
    utf16_sinhala_ci = "utf16_sinhala_ci"
    utf16_slovak_ci = "utf16_slovak_ci"
    utf16_slovenian_ci = "utf16_slovenian_ci"
    utf16_spanish2_ci = "utf16_spanish2_ci"
    utf16_spanish_ci = "utf16_spanish_ci"
    utf16_swedish_ci = "utf16_swedish_ci"
    utf16_turkish_ci = "utf16_turkish_ci"
    utf16_unicode_520_ci = "utf16_unicode_520_ci"
    utf16_unicode_ci = "utf16_unicode_ci"
    utf16_vietnamese_ci = "utf16_vietnamese_ci"
    utf16le_bin = "utf16le_bin"
    utf16le_general_ci = "utf16le_general_ci"
    utf32_bin = "utf32_bin"
    utf32_croatian_ci = "utf32_croatian_ci"
    utf32_czech_ci = "utf32_czech_ci"
    utf32_danish_ci = "utf32_danish_ci"
    utf32_esperanto_ci = "utf32_esperanto_ci"
    utf32_estonian_ci = "utf32_estonian_ci"
    utf32_general_ci = "utf32_general_ci"
    utf32_german2_ci = "utf32_german2_ci"
    utf32_hungarian_ci = "utf32_hungarian_ci"
    utf32_icelandic_ci = "utf32_icelandic_ci"
    utf32_latvian_ci = "utf32_latvian_ci"
    utf32_lithuanian_ci = "utf32_lithuanian_ci"
    utf32_persian_ci = "utf32_persian_ci"
    utf32_polish_ci = "utf32_polish_ci"
    utf32_romanian_ci = "utf32_romanian_ci"
    utf32_roman_ci = "utf32_roman_ci"
    utf32_sinhala_ci = "utf32_sinhala_ci"
    utf32_slovak_ci = "utf32_slovak_ci"
    utf32_slovenian_ci = "utf32_slovenian_ci"
    utf32_spanish2_ci = "utf32_spanish2_ci"
    utf32_spanish_ci = "utf32_spanish_ci"
    utf32_swedish_ci = "utf32_swedish_ci"
    utf32_turkish_ci = "utf32_turkish_ci"
    utf32_unicode_520_ci = "utf32_unicode_520_ci"
    utf32_unicode_ci = "utf32_unicode_ci"
    utf32_vietnamese_ci = "utf32_vietnamese_ci"
    utf8mb3_bin = "utf8mb3_bin"
    utf8mb3_croatian_ci = "utf8mb3_croatian_ci"
    utf8mb3_czech_ci = "utf8mb3_czech_ci"
    utf8mb3_danish_ci = "utf8mb3_danish_ci"
    utf8mb3_esperanto_ci = "utf8mb3_esperanto_ci"
    utf8mb3_estonian_ci = "utf8mb3_estonian_ci"
    utf8mb3_general_ci = "utf8mb3_general_ci"
    utf8mb3_general_mysql500_ci = "utf8mb3_general_mysql500_ci"
    utf8mb3_german2_ci = "utf8mb3_german2_ci"
    utf8mb3_hungarian_ci = "utf8mb3_hungarian_ci"
    utf8mb3_icelandic_ci = "utf8mb3_icelandic_ci"
    utf8mb3_latvian_ci = "utf8mb3_latvian_ci"
    utf8mb3_lithuanian_ci = "utf8mb3_lithuanian_ci"
    utf8mb3_persian_ci = "utf8mb3_persian_ci"
    utf8mb3_polish_ci = "utf8mb3_polish_ci"
    utf8mb3_romanian_ci = "utf8mb3_romanian_ci"
    utf8mb3_roman_ci = "utf8mb3_roman_ci"
    utf8mb3_sinhala_ci = "utf8mb3_sinhala_ci"
    utf8mb3_slovak_ci = "utf8mb3_slovak_ci"
    utf8mb3_slovenian_ci = "utf8mb3_slovenian_ci"
    utf8mb3_spanish2_ci = "utf8mb3_spanish2_ci"
    utf8mb3_spanish_ci = "utf8mb3_spanish_ci"
    utf8mb3_swedish_ci = "utf8mb3_swedish_ci"
    utf8mb3_tolower_ci = "utf8mb3_tolower_ci"
    utf8mb3_turkish_ci = "utf8mb3_turkish_ci"
    utf8mb3_unicode_520_ci = "utf8mb3_unicode_520_ci"
    utf8mb3_unicode_ci = "utf8mb3_unicode_ci"
    utf8mb3_vietnamese_ci = "utf8mb3_vietnamese_ci"
    utf8mb4_0900_ai_ci = "utf8mb4_0900_ai_ci"
    utf8mb4_0900_as_ci = "utf8mb4_0900_as_ci"
    utf8mb4_0900_as_cs = "utf8mb4_0900_as_cs"
    utf8mb4_0900_bin = "utf8mb4_0900_bin"
    utf8mb4_bg_0900_ai_ci = "utf8mb4_bg_0900_ai_ci"
    utf8mb4_bg_0900_as_cs = "utf8mb4_bg_0900_as_cs"
    utf8mb4_bin = "utf8mb4_bin"
    utf8mb4_bs_0900_ai_ci = "utf8mb4_bs_0900_ai_ci"
    utf8mb4_bs_0900_as_cs = "utf8mb4_bs_0900_as_cs"
    utf8mb4_croatian_ci = "utf8mb4_croatian_ci"
    utf8mb4_cs_0900_ai_ci = "utf8mb4_cs_0900_ai_ci"
    utf8mb4_cs_0900_as_cs = "utf8mb4_cs_0900_as_cs"
    utf8mb4_czech_ci = "utf8mb4_czech_ci"
    utf8mb4_danish_ci = "utf8mb4_danish_ci"
    utf8mb4_da_0900_ai_ci = "utf8mb4_da_0900_ai_ci"
    utf8mb4_da_0900_as_cs = "utf8mb4_da_0900_as_cs"
    utf8mb4_de_pb_0900_ai_ci = "utf8mb4_de_pb_0900_ai_ci"
    utf8mb4_de_pb_0900_as_cs = "utf8mb4_de_pb_0900_as_cs"
    utf8mb4_eo_0900_ai_ci = "utf8mb4_eo_0900_ai_ci"
    utf8mb4_eo_0900_as_cs = "utf8mb4_eo_0900_as_cs"
    utf8mb4_esperanto_ci = "utf8mb4_esperanto_ci"
    utf8mb4_estonian_ci = "utf8mb4_estonian_ci"
    utf8mb4_es_0900_ai_ci = "utf8mb4_es_0900_ai_ci"
    utf8mb4_es_0900_as_cs = "utf8mb4_es_0900_as_cs"
    utf8mb4_es_trad_0900_ai_ci = "utf8mb4_es_trad_0900_ai_ci"
    utf8mb4_es_trad_0900_as_cs = "utf8mb4_es_trad_0900_as_cs"
    utf8mb4_et_0900_ai_ci = "utf8mb4_et_0900_ai_ci"
    utf8mb4_et_0900_as_cs = "utf8mb4_et_0900_as_cs"
    utf8mb4_general_ci = "utf8mb4_general_ci"
    utf8mb4_german2_ci = "utf8mb4_german2_ci"
    utf8mb4_gl_0900_ai_ci = "utf8mb4_gl_0900_ai_ci"
    utf8mb4_gl_0900_as_cs = "utf8mb4_gl_0900_as_cs"
    utf8mb4_hr_0900_ai_ci = "utf8mb4_hr_0900_ai_ci"
    utf8mb4_hr_0900_as_cs = "utf8mb4_hr_0900_as_cs"
    utf8mb4_hungarian_ci = "utf8mb4_hungarian_ci"
    utf8mb4_hu_0900_ai_ci = "utf8mb4_hu_0900_ai_ci"
    utf8mb4_hu_0900_as_cs = "utf8mb4_hu_0900_as_cs"
    utf8mb4_icelandic_ci = "utf8mb4_icelandic_ci"
    utf8mb4_is_0900_ai_ci = "utf8mb4_is_0900_ai_ci"
    utf8mb4_is_0900_as_cs = "utf8mb4_is_0900_as_cs"
    utf8mb4_ja_0900_as_cs = "utf8mb4_ja_0900_as_cs"
    utf8mb4_ja_0900_as_cs_ks = "utf8mb4_ja_0900_as_cs_ks"
    utf8mb4_latvian_ci = "utf8mb4_latvian_ci"
    utf8mb4_la_0900_ai_ci = "utf8mb4_la_0900_ai_ci"
    utf8mb4_la_0900_as_cs = "utf8mb4_la_0900_as_cs"
    utf8mb4_lithuanian_ci = "utf8mb4_lithuanian_ci"
    utf8mb4_lt_0900_ai_ci = "utf8mb4_lt_0900_ai_ci"
    utf8mb4_lt_0900_as_cs = "utf8mb4_lt_0900_as_cs"
    utf8mb4_lv_0900_ai_ci = "utf8mb4_lv_0900_ai_ci"
    utf8mb4_lv_0900_as_cs = "utf8mb4_lv_0900_as_cs"
    utf8mb4_mn_cyrl_0900_ai_ci = "utf8mb4_mn_cyrl_0900_ai_ci"
    utf8mb4_mn_cyrl_0900_as_cs = "utf8mb4_mn_cyrl_0900_as_cs"
    utf8mb4_nb_0900_ai_ci = "utf8mb4_nb_0900_ai_ci"
    utf8mb4_nb_0900_as_cs = "utf8mb4_nb_0900_as_cs"
    utf8mb4_nn_0900_ai_ci = "utf8mb4_nn_0900_ai_ci"
    utf8mb4_nn_0900_as_cs = "utf8mb4_nn_0900_as_cs"
    utf8mb4_persian_ci = "utf8mb4_persian_ci"
    utf8mb4_pl_0900_ai_ci = "utf8mb4_pl_0900_ai_ci"
    utf8mb4_pl_0900_as_cs = "utf8mb4_pl_0900_as_cs"
    utf8mb4_polish_ci = "utf8mb4_polish_ci"
    utf8mb4_romanian_ci = "utf8mb4_romanian_ci"
    utf8mb4_roman_ci = "utf8mb4_roman_ci"
    utf8mb4_ro_0900_ai_ci = "utf8mb4_ro_0900_ai_ci"
    utf8mb4_ro_0900_as_cs = "utf8mb4_ro_0900_as_cs"
    utf8mb4_ru_0900_ai_ci = "utf8mb4_ru_0900_ai_ci"
    utf8mb4_ru_0900_as_cs = "utf8mb4_ru_0900_as_cs"
    utf8mb4_sinhala_ci = "utf8mb4_sinhala_ci"
    utf8mb4_sk_0900_ai_ci = "utf8mb4_sk_0900_ai_ci"
    utf8mb4_sk_0900_as_cs = "utf8mb4_sk_0900_as_cs"
    utf8mb4_slovak_ci = "utf8mb4_slovak_ci"
    utf8mb4_slovenian_ci = "utf8mb4_slovenian_ci"
    utf8mb4_sl_0900_ai_ci = "utf8mb4_sl_0900_ai_ci"
    utf8mb4_sl_0900_as_cs = "utf8mb4_sl_0900_as_cs"
    utf8mb4_spanish2_ci = "utf8mb4_spanish2_ci"
    utf8mb4_spanish_ci = "utf8mb4_spanish_ci"
    utf8mb4_sr_latn_0900_ai_ci = "utf8mb4_sr_latn_0900_ai_ci"
    utf8mb4_sr_latn_0900_as_cs = "utf8mb4_sr_latn_0900_as_cs"
    utf8mb4_sv_0900_ai_ci = "utf8mb4_sv_0900_ai_ci"
    utf8mb4_sv_0900_as_cs = "utf8mb4_sv_0900_as_cs"
    utf8mb4_swedish_ci = "utf8mb4_swedish_ci"
    utf8mb4_tr_0900_ai_ci = "utf8mb4_tr_0900_ai_ci"
    utf8mb4_tr_0900_as_cs = "utf8mb4_tr_0900_as_cs"
    utf8mb4_turkish_ci = "utf8mb4_turkish_ci"
    utf8mb4_unicode_520_ci = "utf8mb4_unicode_520_ci"
    utf8mb4_unicode_ci = "utf8mb4_unicode_ci"
    utf8mb4_vietnamese_ci = "utf8mb4_vietnamese_ci"
    utf8mb4_vi_0900_ai_ci = "utf8mb4_vi_0900_ai_ci"
    utf8mb4_vi_0900_as_cs = "utf8mb4_vi_0900_as_cs"
    utf8mb4_zh_0900_as_cs = "utf8mb4_zh_0900_as_cs"


class MySQLDbAdd(BaseModel):
    database_name: str = Field(..., description="Database name")
    collate: MySQLCollate | None = Field(
        None, description="Optional collation, passed as --collate="
    )


class MySQLUserAdd(BaseModel):
    user_name: str = Field(..., description="MySQL username")
    password: str | None = Field(
        None, description="Plaintext password, generated randomly if not provided"
    )


class MySQLAccessAdd(BaseModel):
    user_name: str = Field(..., description="Username")
    host_name: str = Field(..., description="Host or IP")


class MySQLPrivileges(BaseModel):
    user_name: str = Field(..., description="Username")
    host_name: str | None = Field(None, description="Optional host part")
    database_name: str = Field(..., description="DB name")
    mysql_privileges: list[str] = Field(
        ...,
        description=(
            "List of privilege operations. Each element must be of the form +PRIV or -PRIV. "
            "Allowed PRIV values: ALL, SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, DROP, "
            "CREATE_TEMPORARY_TABLES, SHOW_VIEW, CREATE_ROUTINE, ALTER_ROUTINE, EXECUTE, CREATE_VIEW, "
            "EVENT, TRIGGER, LOCK_TABLES, REFERENCES. Use exactly one entry when using +ALL or -ALL."
        ),
        examples=[["+ALL"], ["+SELECT", "+INSERT"], ["-DELETE"]],
    )

    class Privilege(str, Enum):
        ALL = "ALL"
        SELECT = "SELECT"
        INSERT = "INSERT"
        UPDATE = "UPDATE"
        DELETE = "DELETE"
        CREATE = "CREATE"
        ALTER = "ALTER"
        INDEX = "INDEX"
        DROP = "DROP"
        CREATE_TEMPORARY_TABLES = "CREATE_TEMPORARY_TABLES"
        SHOW_VIEW = "SHOW_VIEW"
        CREATE_ROUTINE = "CREATE_ROUTINE"
        ALTER_ROUTINE = "ALTER_ROUTINE"
        EXECUTE = "EXECUTE"
        CREATE_VIEW = "CREATE_VIEW"
        EVENT = "EVENT"
        TRIGGER = "TRIGGER"
        LOCK_TABLES = "LOCK_TABLES"
        REFERENCES = "REFERENCES"

    _privilege_pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"^[+-](?:" + "|".join(p.value for p in Privilege) + r")$"
    )

    @field_validator("mysql_privileges")
    @classmethod
    def validate_mysql_privileges(cls, value: list[str]):
        # Ensure list not empty
        if not value:
            raise ValueError("At least one privilege operation must be provided")

        seen: set[str] = set()
        cleaned: list[str] = []
        has_all = any(v.endswith("ALL") for v in value)
        if has_all and len(value) > 1:
            raise ValueError("+ALL or -ALL must be the only privilege if specified")
        for item in value:
            if not isinstance(item, str):
                raise ValueError("Privilege entries must be strings")
            item = item.strip().upper()
            if not cls._privilege_pattern.match(item):
                raise ValueError(
                    f"Invalid privilege spec '{item}'. Expect +|-(PRIVILEGE)"
                )
            # Disallow both +PRIV and -PRIV combinations for same privilege
            base = item[1:]
            if base == "ALL" and len(value) > 1:
                raise ValueError("ALL cannot be combined with other privileges")
            # Prevent contradictory ops on same privilege
            if any(prev[1:] == base and prev[0] != item[0] for prev in cleaned):
                raise ValueError(
                    f"Conflicting privilege operations for '{base}' specified"
                )
            if item not in seen:
                seen.add(item)
                cleaned.append(item)
        return cleaned


class MySQLPasswd(BaseModel):
    user_name: str = Field(..., description="Username")
    host_name: str | None = Field(None, description="Optional host part")
    password: str | None = Field(
        None, description="New password, generated randomly if not provided"
    )
