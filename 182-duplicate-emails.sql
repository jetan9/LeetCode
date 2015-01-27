select Email from
(select count(*) as Num, Email from Person group by Email) t
where t.Num>1