CREATE TABLE agents (
    agent_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    fullname VARCHAR(255) NOT NULL
);

CREATE TABLE shifts (
    shift_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    agent_id BIGINT NOT NULL REFERENCES agents(agent_id) ON DELETE CASCADE,
    shift_date DATE NOT NULL,
    clock_in TIME ,
    clock_out TIME ,
    UNIQUE (agent_id,shift_date)
);

CREATE TABLE events (
    event_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    shift_id INT NOT NULL REFERENCES shifts(shift_id) ON DELETE CASCADE,
    event VARCHAR(50) NOT NULL,
    event_time TIME NOT NULL,
    UNIQUE (shift_id,event_time)
);


CREATE TABLE shift_swaps(
    swap_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    requester BIGINT REFERENCES agents (agent_id),
    shift_owner BIGINT REFERENCES agents(agent_id),
    swap_status VARCHAR NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP 

);

CREATE TABLE swap_items(
    swap_item_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    swap_id BIGINT NOT NULL REFERENCES shift_swaps(swap_id) ON DELETE CASCADE,
    wanted_shift BIGINT NOT NULL REFERENCES shifts(shift_id),
    offer BIGINT NOT NULL REFERENCES shifts(shift_id)
);