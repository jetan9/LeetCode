select d.Name as Department, f.Employee, f.Salary from `Department` as d inner join
(select e.DepartmentId, e.Name as Employee, e.Salary from Employee as e inner join 
(select DepartmentId,max(Salary) as Salary from Employee group by DepartmentId) as t 
on e.DepartmentId=t.DepartmentId and e.Salary=t.Salary) as f
on d.Id=f.DepartmentId