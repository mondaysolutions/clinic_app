create view v_student_history as
select
    e.student_history_id, e.student_id, e.teacher_id,
    f.first_name || " " || f.last_name as student_name,
    e.teacher_name, e.instrument, e.grade,
    e.start_date,
    -- e.lesson_week,
    CASE e.lesson_week
     WHEN 0 THEN 'Monday'
     WHEN 1 THEN 'Tuesday'
     WHEN 2 THEN 'Wednesday'
     WHEN 3 THEN 'Thursday'
     WHEN 4 THEN 'Friday'
     WHEN 5 THEN 'Saturday'
     WHEN 6 THEN 'Sunday'
    END as lesson_week,
    e.lesson_begin_time, e.lesson_end_time, e.lesson_duration
from (
    select
        c.student_history_id, c.student_id, c.teacher_id,
        d.first_name || " " || d.last_name as teacher_name,
        c.instrument, c.grade,
        c.start_date, c.lesson_week, c.lesson_begin_time, c.lesson_end_time, c.lesson_duration
    from (
        select
            a.student_history_id, a.student_id, a.teacher_id, a.instrument, b.name as grade,
            a.start_date, a.lesson_week, a.lesson_begin_time, a.lesson_end_time, a.lesson_duration
        from (
            select
                h.id as student_history_id, h.student_id, h.teacher_id, i.name as instrument, h.grade_id,
                h.start_date, h.lesson_week, h.lesson_begin_time, h.lesson_end_time, h.lesson_duration
            from
                student_history h
            inner join
                instrument i on
            i.id = h.instrument_id
        ) a
        inner join
        grade b on
        a.grade_id = b.id
    ) c
    inner join
    teacher d on
    c.teacher_id = d.id
) e
inner join
student f on
e.student_id = f.id
;


create view view_lesson_fee as
select
    d.name as instrument, c.grade, c.price, c.duration
from (
    select a.instrument_id, b.name as grade, a.price, a.duration
    from
    lesson_fee a
    left join
    grade b
    on a.grade_id = b.id
) c
left join
instrument d on
c.instrument_id = d.id
;