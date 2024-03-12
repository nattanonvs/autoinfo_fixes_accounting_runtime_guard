from odoo import api, models, fields
from odoo import tools


class auto_generate_function(models.AbstractModel):
    _name = 'auto.generate.function'
    _description = 'auto.generate.function'
    _auto = False

    def init(self):

        self.env.cr.execute("""CREATE OR REPLACE FUNCTION convert_num_th_with_currency(val numeric, currency_id int)
            RETURNS character AS
            $BODY$
            DECLARE
            bahtTH varchar DEFAULT '';
            numberVAl integer DEFAULT 0;
            intVal varchar(50);
            decVal varchar(50);
            unit_label varchar default '';
            sub_label varchar default '';

            i integer := 0;
            iLen integer;
            BEGIN
            BEGIN
            CREATE TEMP TABLE num
            (
            Id integer,
            Text varchar(50)
            );
            INSERT INTO num VALUES (0, '');
            INSERT INTO num VALUES (1, 'หนึ่ง');
            INSERT INTO num VALUES (2, 'สอง');
            INSERT INTO num VALUES (3, 'สาม');
            INSERT INTO num VALUES (4, 'สี่');
            INSERT INTO num VALUES (5, 'ห้า');
            INSERT INTO num VALUES (6, 'หก');
            INSERT INTO num VALUES (7, 'เจ็ด');
            INSERT INTO num VALUES (8, 'แปด');
            INSERT INTO num VALUES (9, 'เก้า');
            INSERT INTO num VALUES (10, 'สิบ');
            END;

            BEGIN
            CREATE TEMP TABLE rank
            (
            Id integer,
            Text varchar(50)
            );
            INSERT INTO rank VALUES (0, '');
            INSERT INTO rank VALUES (1, 'สิบ');
            INSERT INTO rank VALUES (2, 'ร้อย');
            INSERT INTO rank VALUES (3, 'พัน');
            INSERT INTO rank VALUES (4, 'หมื่น');
            INSERT INTO rank VALUES (5, 'แสน');
            INSERT INTO rank VALUES (6, 'ล้าน');
            INSERT INTO rank VALUES (7, 'สิบ');
            INSERT INTO rank VALUES (8, 'ร้อย');
            INSERT INTO rank VALUES (9, 'พัน');
            END;

            intVal := split_part(cast(val as text), '.', 1);
            decVal := split_part(cast(val as text), '.', 2);

            select coalesce(currency_unit_label, 'บาท'), coalesce(currency_subunit_label, 'สตางค์')
            into unit_label, sub_label
            from res_currency
            where id = currency_id;

            IF(val = 0) THEN
            bahtTH := CONCAT('ศูนย์', unit_label, 'ถ้วน');
            ELSE
            iLen := LENGTH(intVal);

            WHILE (i < iLen) LOOP
            numberVAl := CAST(SUBSTRING(intVal, i + 1, 1) AS INTEGER);
            IF(numberVAl <> 0) THEN
            IF((i = (LENGTH(intVal) - 1)) AND (numberVAl = 1)) THEN
            IF(LENGTH(intVal) = 1) THEN
            bahtTH := CONCAT(bahtTH,'หนึ่ง');
            ELSE
            bahtTH := CONCAT(bahtTH, 'เอ็ด');
            END IF;
            ELSIF((i = (LENGTH(intVal) - 7)) AND (numberVAl = 1)) THEN
            IF(LENGTH(intVal) = 7) THEN
            bahtTH := CONCAT(bahtTH,'หนึ่ง');
            ELSE
            bahtTH := CONCAT(bahtTH, 'เอ็ด');
            END IF;
            ELSIF((i = (LENGTH(intVal) - 2)) AND (numberVAl = 2)) THEN
            bahtTH := CONCAT(bahtTH,'ยี่');
            ELSIF((i = (LENGTH(intVal) - 8)) AND (numberVAl = 2)) THEN
            bahtTH := CONCAT(bahtTH,'ยี่');
            ELSIF((i = (LENGTH(intVal) - 2)) AND (numberVAl = 1)) THEN
            bahtTH := CONCAT(bahtTH,'');
            ELSIF((i = (LENGTH(intVal) - 8)) AND (numberVAl = 1)) THEN
            bahtTH := CONCAT(bahtTH,'');
            ELSE
            bahtTH := CONCAT(bahtTH, (SELECT Text FROM num WHERE Id = numberVAl Limit 1));
            END IF;

            bahtTH := CONCAT(bahtTH, (SELECT Text FROM rank WHERE Id = ((LENGTH(intVal) - i) - 1) Limit 1));

			ELSE
            IF (i = (LENGTH(intVal) - 7)) THEN
            bahtTH := CONCAT(bahtTH,'ล้าน');
			END IF;
            END IF;
            i := i + 1;
            END LOOP;

            bahtTH := CONCAT(bahtTH, unit_label);
            IF(length(decVal) = 0) or (CAST(decVal as integer) = 0) THEN
            bahtTH := CONCAT(bahtTH, 'ถ้วน');
            ELSIF (SUBSTRING(decVal, 1, 1) = '0') THEN
            numberVAl := CAST(SUBSTRING(decVal, 2, 1) AS INTEGER);
            bahtTH := CONCAT(bahtTH, (SELECT Text FROM num WHERE Id = numberVAl Limit 1));
            bahtTH := CONCAT(bahtTH, sub_label);
            ELSE
            i := 0;
            WHILE (i < iLen) LOOP
            numberVAl := CAST(SUBSTRING(decVal, i + 1, 1) AS INTEGER);
            iLen := LENGTH(decVal);
            IF(numberVAl <> 0) THEN
            IF((i = (LENGTH(decVal) - 1)) AND (numberVAl = 1)) THEN
            bahtTH := CONCAT(bahtTH, 'เอ็ด');
            ELSIF((i = (LENGTH(decVal) - 2)) AND (numberVAl = 2)) THEN
            bahtTH := CONCAT(bahtTH, 'ยี่');
            ELSIF((i = (LENGTH(decVal) - 2)) AND (numberVAl = 1)) THEN
            bahtTH := CONCAT(bahtTH, '');
            ELSE
            bahtTH := CONCAT(bahtTH, (SELECT Text FROM num WHERE Id = numberVAl Limit 1));
            END IF;

            bahtTH := CONCAT(bahtTH, (SELECT Text FROM rank WHERE Id = ((LENGTH(decVal) - i) - 1) Limit 1));
            END IF;
            i := i + 1;
            END LOOP;
            bahtTH := CONCAT(bahtTH, sub_label);
            END IF;
            END IF;

            DROP TABLE num;
            DROP TABLE rank;
            RETURN bahtTH;
            END;
            $BODY$
            LANGUAGE plpgsql;""")

        self.env.cr.execute("""CREATE OR REPLACE FUNCTION convert_num_th(val numeric)
            RETURNS character AS
            $BODY$
            DECLARE
            bahtTH varchar DEFAULT '';
            numberVAl integer DEFAULT 0;
            intVal varchar(50);
            decVal varchar(50);

            i integer := 0;
            iLen integer;
            BEGIN
            BEGIN
            CREATE TEMP TABLE num
            (
            Id integer,
            Text varchar(50)
            );
            INSERT INTO num VALUES (0, '');
            INSERT INTO num VALUES (1, 'หนึ่ง');
            INSERT INTO num VALUES (2, 'สอง');
            INSERT INTO num VALUES (3, 'สาม');
            INSERT INTO num VALUES (4, 'สี่');
            INSERT INTO num VALUES (5, 'ห้า');
            INSERT INTO num VALUES (6, 'หก');
            INSERT INTO num VALUES (7, 'เจ็ด');
            INSERT INTO num VALUES (8, 'แปด');
            INSERT INTO num VALUES (9, 'เก้า');
            INSERT INTO num VALUES (10, 'สิบ');
            END;

            BEGIN
            CREATE TEMP TABLE rank
            (
            Id integer,
            Text varchar(50)
            );
            INSERT INTO rank VALUES (0, '');
            INSERT INTO rank VALUES (1, 'สิบ');
            INSERT INTO rank VALUES (2, 'ร้อย');
            INSERT INTO rank VALUES (3, 'พัน');
            INSERT INTO rank VALUES (4, 'หมื่น');
            INSERT INTO rank VALUES (5, 'แสน');
            INSERT INTO rank VALUES (6, 'ล้าน');
            INSERT INTO rank VALUES (7, 'สิบ');
            INSERT INTO rank VALUES (8, 'ร้อย');
            INSERT INTO rank VALUES (9, 'พัน');
            END;

            intVal := split_part(cast(val as text), '.', 1);
            decVal := split_part(cast(val as text), '.', 2);

            IF(val = 0) THEN
            bahtTH := 'ศูนย์บาทถ้วน';
            ELSE
            iLen := LENGTH(intVal);

            WHILE (i < iLen) LOOP
            numberVAl := CAST(SUBSTRING(intVal, i + 1, 1) AS INTEGER);
            IF(numberVAl <> 0) THEN
            IF((i = (LENGTH(intVal) - 1)) AND (numberVAl = 1)) THEN
            IF(LENGTH(intVal) = 1) THEN
            bahtTH := CONCAT(bahtTH,'หนึ่ง');
            ELSE
            bahtTH := CONCAT(bahtTH, 'เอ็ด');
            END IF;
            ELSIF((i = (LENGTH(intVal) - 7)) AND (numberVAl = 1)) THEN
            IF(LENGTH(intVal) = 7) THEN
            bahtTH := CONCAT(bahtTH,'หนึ่ง');
            ELSE
            bahtTH := CONCAT(bahtTH, 'เอ็ด');
            END IF;
            ELSIF((i = (LENGTH(intVal) - 2)) AND (numberVAl = 2)) THEN
            bahtTH := CONCAT(bahtTH,'ยี่');
            ELSIF((i = (LENGTH(intVal) - 8)) AND (numberVAl = 2)) THEN
            bahtTH := CONCAT(bahtTH,'ยี่');
            ELSIF((i = (LENGTH(intVal) - 2)) AND (numberVAl = 1)) THEN
            bahtTH := CONCAT(bahtTH,'');
            ELSIF((i = (LENGTH(intVal) - 8)) AND (numberVAl = 1)) THEN
            bahtTH := CONCAT(bahtTH,'');
            ELSE
            bahtTH := CONCAT(bahtTH, (SELECT Text FROM num WHERE Id = numberVAl Limit 1));
            END IF;

            bahtTH := CONCAT(bahtTH, (SELECT Text FROM rank WHERE Id = ((LENGTH(intVal) - i) - 1) Limit 1));

			ELSE
            IF (i = (LENGTH(intVal) - 7)) THEN
            bahtTH := CONCAT(bahtTH,'ล้าน');
			END IF;
            END IF;
            i := i + 1;
            END LOOP;

            bahtTH := CONCAT(bahtTH, 'บาท');
            IF(length(decVal) = 0) or (CAST(decVal as integer) = 0) THEN
            bahtTH := CONCAT(bahtTH, 'ถ้วน');
            ELSIF (SUBSTRING(decVal, 1, 1) = '0') THEN
            numberVAl := CAST(SUBSTRING(decVal, 2, 1) AS INTEGER);
            bahtTH := CONCAT(bahtTH, (SELECT Text FROM num WHERE Id = numberVAl Limit 1));
            bahtTH := CONCAT(bahtTH, 'สตางค์');
            ELSE
            i := 0;
            WHILE (i < iLen) LOOP
            numberVAl := CAST(SUBSTRING(decVal, i + 1, 1) AS INTEGER);
            iLen := LENGTH(decVal);
            IF(numberVAl <> 0) THEN
            IF((i = (LENGTH(decVal) - 1)) AND (numberVAl = 1)) THEN
            bahtTH := CONCAT(bahtTH, 'เอ็ด');
            ELSIF((i = (LENGTH(decVal) - 2)) AND (numberVAl = 2)) THEN
            bahtTH := CONCAT(bahtTH, 'ยี่');
            ELSIF((i = (LENGTH(decVal) - 2)) AND (numberVAl = 1)) THEN
            bahtTH := CONCAT(bahtTH, '');
            ELSE
            bahtTH := CONCAT(bahtTH, (SELECT Text FROM num WHERE Id = numberVAl Limit 1));
            END IF;

            bahtTH := CONCAT(bahtTH, (SELECT Text FROM rank WHERE Id = ((LENGTH(decVal) - i) - 1) Limit 1));
            END IF;
            i := i + 1;
            END LOOP;
            bahtTH := CONCAT(bahtTH,'สตางค์');
            END IF;
            END IF;

            DROP TABLE num;
            DROP TABLE rank;
            RETURN bahtTH;
            END;
            $BODY$
            LANGUAGE plpgsql;""")
