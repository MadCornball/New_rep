create table if not exists users
(
    user_id    integer not null
        primary key,
    username   varchar(255),
    password   varchar(255),
    email      varchar(255),
    created_at timestamp
);

alter table users
    owner to postgres;

create table if not exists conversations
(
    conversation_id integer not null
        primary key,
    user_id         integer
        references users,
    started_at      timestamp,
    ended_at        timestamp,
    status          varchar(255)
);

alter table conversations
    owner to postgres;

create table if not exists messages
(
    message_id      integer not null
        primary key,
    conversation_id integer
        references conversations,
    user_id         integer
        references users,
    content         text,
    created_at      timestamp
);

alter table messages
    owner to postgres;

create table if not exists neuralnetworks
(
    network_id  integer not null
        primary key,
    name        varchar(255),
    description text,
    created_by  integer
        references users,
    created_at  timestamp
);

alter table neuralnetworks
    owner to postgres;

create table if not exists networkresponses
(
    response_id integer not null
        primary key,
    network_id  integer
        references neuralnetworks,
    message_id  integer
        references messages,
    content     text,
    created_at  timestamp
);

alter table networkresponses
    owner to postgres;

