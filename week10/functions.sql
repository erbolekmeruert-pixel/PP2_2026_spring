
CREATE OR REPLACE FUNCTION search_contacts(p_pattern TEXT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone
    FROM phonebook p
    WHERE p.name ILIKE '%' || p_pattern || '%'
       OR p.phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone
    FROM phonebook p
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;