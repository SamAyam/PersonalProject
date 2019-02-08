using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class GetTasks : MonoBehaviour {
    public TaskObject blankTask;
    public bool optional;
    public int repeatType;  // 0 = none(all), 1 = daily, 2 = weekly, 3 = monthly, 4 = yearly
    public int numberOfDays;  // 0 = all, 1 = today, 2 = thisWeek, 3 = thisMonth, 4 = thisYear
    public TaskButtonsScript selectedScript;
    
    public void SelectTask(TaskObject task)
    {
        selectedScript.selectedList.Add(task);
    }

    public void DeselectTask(TaskObject task)
    {
        selectedScript.selectedList.Remove(task);
    }

    public void DrawTasks()
    {
        if (AppControl.control != null)
        {
            Clear();
            AppControl.control.tasksList.Sort((p1, p2) => p1.dueDate.CompareTo(p2.dueDate));
            for (int i = 0; i < AppControl.control.tasksList.Count; i++)
            {
                if (repeatType == 0) // 0 = show all
                {
                    if (AppControl.control.tasksList[i].optional == optional)
                    {
                        MakeTask(i);
                    }
                }
                else if (repeatType == 1) // 1 = daily 
                {
                    if (AppControl.control.tasksList[i].optional == optional 
                        && (AppControl.control.tasksList[i].repeatType == 1 || AppControl.control.tasksList[i].repeatType == 0))
                    {
                        if (numberOfDays == 0 ||
                            (numberOfDays == 1 && AppControl.control.tasksList[i].dueDate.Date.Subtract(DateTime.Today).Days < 0) ||
                            (numberOfDays == 2 && AppControl.control.tasksList[i].dueDate.Date.Subtract(DateTime.Today).Days < 7) ||
                            (numberOfDays == 3 && AppControl.control.tasksList[i].dueDate.Month == DateTime.Today.Month) ||
                            (numberOfDays == 4 && AppControl.control.tasksList[i].dueDate.Year == DateTime.Today.Year))
                        {
                            MakeTask(i);
                        }
                    }
                }

                else if (repeatType == 2) // 2 = weekly 
                {
                    if (AppControl.control.tasksList[i].optional == optional && (AppControl.control.tasksList[i].repeatType == 2))
                    {
                        if (numberOfDays == 0 ||
                            (numberOfDays == 1 && AppControl.control.tasksList[i].dueDate == DateTime.Today) ||
                            (numberOfDays == 2 && AppControl.control.tasksList[i].dueDate.Date.Subtract(DateTime.Today).Days < 7) ||
                            (numberOfDays == 3 && AppControl.control.tasksList[i].dueDate.Month == DateTime.Today.Month) ||
                            (numberOfDays == 4 && AppControl.control.tasksList[i].dueDate.Year == DateTime.Today.Year))
                        {
                            MakeTask(i);
                        }
                    }
                }

                else if (repeatType == 3) // 3 = monthly 
                {
                    if (AppControl.control.tasksList[i].optional == optional && (AppControl.control.tasksList[i].repeatType == 2))
                    {
                        if (numberOfDays == 0 ||
                            (numberOfDays == 1 && AppControl.control.tasksList[i].dueDate == DateTime.Today) ||
                            (numberOfDays == 2 && AppControl.control.tasksList[i].dueDate.Date.Subtract(DateTime.Today).Days < 7) ||
                            (numberOfDays == 3 && AppControl.control.tasksList[i].dueDate.Month == DateTime.Today.Month) ||
                            (numberOfDays == 4 && AppControl.control.tasksList[i].dueDate.Year == DateTime.Today.Year))
                        {
                            MakeTask(i);
                        }
                    }
                }

                else if (repeatType == 4) // 4 = yearly 
                {
                    if (AppControl.control.tasksList[i].optional == optional && AppControl.control.tasksList[i].dueDate.Year == DateTime.Today.Year
                       && (AppControl.control.tasksList[i].repeatType == 2))
                    {
                        if (numberOfDays == 0 ||
                            (numberOfDays == 1 && AppControl.control.tasksList[i].dueDate == DateTime.Today) ||
                            (numberOfDays == 2 && AppControl.control.tasksList[i].dueDate.Date.Subtract(DateTime.Today).Days < 7) ||
                            (numberOfDays == 3 && AppControl.control.tasksList[i].dueDate.Month == DateTime.Today.Month) ||
                            (numberOfDays == 4 && AppControl.control.tasksList[i].dueDate.Year == DateTime.Today.Year))
                        {
                            MakeTask(i);
                        }
                    }
                }

                else
                {
                    MakeTask(i);
                }
            }
            
        }
    }

    public void MakeTask(int i)
    {
        TaskObject newTaskInstance = Instantiate(blankTask) as TaskObject;
        newTaskInstance.myTask = AppControl.control.tasksList[i];
        newTaskInstance.taskFolder = AppControl.control.tasksList[i].taskFolder;
        newTaskInstance.taskName = AppControl.control.tasksList[i].taskName;
        newTaskInstance.dueDate = AppControl.control.tasksList[i].dueDate;
        newTaskInstance.optional = AppControl.control.tasksList[i].optional;
        newTaskInstance.repeatType = AppControl.control.tasksList[i].repeatType;
        newTaskInstance.priority = AppControl.control.tasksList[i].priority;
        newTaskInstance.userTags = AppControl.control.tasksList[i].userTags;
        newTaskInstance.transform.SetParent(this.transform);
        newTaskInstance.GetComponent<RectTransform>().localScale = Vector3.one;
        newTaskInstance.Resize();
    }

    public void Clear()
    {
        foreach (Transform child in transform)
        {
            GameObject.Destroy(child.gameObject);
        }
    }

    private void OnEnable()
    {
        selectedScript.selectedList = new List<TaskObject>();
        DrawTasks();
    }

    private void OnDisable()
    {
        Clear();
    }
}
