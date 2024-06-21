"""module with sql queries"""

SQL_PROCESSING = """
--  creating and preparing tables
drop table if exists mt4_filtered;
drop table if exists mt5_filtered;
drop table if exists mt45;


create temp table mt4_filtered as (
select
    t1.ticket::bigint as ticket,
    t1.login,
    t1.symbol,
    t1.open_time::timestamp as open_time,
    t1.close_time::timestamp as close_time,
    t1.cmd::smallint as cmd
from
    hr_vacancies.mt4_trades t1
left join hr_vacancies.mt4_marked_trades t2 on
    t1.ticket = t2.positionid
where
    1 = 1
    and t1.open_time is not null
    and (t1.close_time is null
        or t1.close_time::timestamp > t1.open_time::timestamp
        or t1.close_time::timestamp = '1970-01-01 00:00:00')
    and (t2.type::integer & 2) = 2
);

create temp table mt5_filtered as (
with op_t as (
select
    t1.positionid,
    t1.login,
    t1.symbol,
    t1.action,
    min(t1.time) as open_time
from
    hr_vacancies.mt5_deals t1
where
    t1.entry = '0'
group by
    t1.positionid,
    t1.login,
    t1.symbol,
    t1.action),

cl_t as (
select
    t2.positionid,
    t2.login,
    t2.symbol,
    t2.action,
    max(time) as close_time
from
    hr_vacancies.mt5_deals t2
where
    t2.entry = '1'
group by
    t2.positionid,
    t2.login,
    t2.symbol,
    t2.action)
select
    op_t.positionid::bigint as ticket,
    op_t.login,
    op_t.symbol,
    open_time::timestamp,
    close_time::timestamp,
    op_t.action::smallint as cmd
from
    op_t
left join cl_t 
on
    1 = 1
    and op_t.positionid = cl_t.positionid
    and op_t.login = cl_t.login
    and op_t.symbol = cl_t.symbol
left join hr_vacancies.mt5_marked_trades mk 
on
    op_t.positionid = mk.positionid
where
    1 = 1
    and open_time is not null
    and (close_time is null
        or close_time::timestamp > open_time::timestamp)
    and ((mk.type::integer & 2) = 2)
);

create temp table mt45 as (
select
    *,
    'mt5' as source
from
    mt5_filtered
union
select
    *,
    'mt4' as source
from
    mt4_filtered
);

"""

SQL_SOLUTION_1 = """
-- SQL for solution 1
select
    login,
    count(login) as num_of_deals_1_min
from
    mt45
where
    close_time - open_time < interval '1 minute'
group by
    login
order by
    1;
"""

SQL_SOLUTION_2 = """
-- SQL for solution 2
select
    f.login,
    count(*) as num_of_unordered_pairs_of_deals_30_s
from
    mt45 f
inner join mt45 s 
on
    f.login = s.login
    and f.ticket > s.ticket
where
    (f.open_time - s.open_time) < interval '30 seconds'
    and (f.open_time - s.open_time) > -interval '30 seconds'
group by
    f.login
order by
    1;
"""

SQL_SOLUTION_3 = """
-- SQL for solution 3
with interval_data as (
select
    mt45.*,
    floor(extract(epoch
from
    mt45.open_time) / 30) as interval_30_s
from
    mt45
),
deal_pairs as (
select
    t1.ticket as ticket1,
    t1.login as login1,
    t1.cmd as cmd1,
    t2.ticket as ticket2,
    t2.login as login2,
    t2.cmd as cmd2,
    t1.symbol as symbol,
    t1.interval_30_s
from
    interval_data t1
join interval_data t2 
    on
    t1.symbol = t2.symbol
    and t1.login > t2.login
    --unordered pairs
    and t1.cmd <> t2.cmd
    and t1.interval_30_s = t2.interval_30_s
),
grouped_deals as (
select
    login1,
    login2,
    symbol,
    interval_30_s,
    count(*) as pair_deals_count
from
    deal_pairs
group by
    login1,
    login2,
    symbol,
    interval_30_s
)
select
    distinct login1,
    login2
from
    grouped_deals
where
    pair_deals_count >= 10;
"""