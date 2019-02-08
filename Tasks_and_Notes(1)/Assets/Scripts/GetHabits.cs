using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class GetHabits : MonoBehaviour
{
    public HabitObject blankHabit;
    public int repeatType;          // This can be 4 (yearly), 3 (monthly), 2 (weekly), 1 (daily), 0 (constant)
    public bool goodHabit = true;
    private List<HabitObject> targetList;

    public NewHabitScript editHabitWindow;
    public GameObject saveHabitButton;

    public HabitButtonsScript selectedScript;

    public void SelectHabit(HabitObject habit)
    {
        selectedScript.selectedList.Add(habit);
    }

    public void DeselectHabit(HabitObject habit)
    {
        selectedScript.selectedList.Remove(habit);
    }

    public void DrawTasks()
    {
        if (AppControl.control != null)
        {
            Clear();
            if (goodHabit)
            {
                targetList = AppControl.control.habitsList;
            }
            else
            {
                targetList = AppControl.control.snapsList;
            }
            
            for (int i = 0; i < targetList.Count; i++)
            {
                if(repeatType == 1)         // Daily panel shows 1 and 0 (daily and constant)
                {
                    if (((targetList[i].repeatType == 1 && targetList[i].done == false) || targetList[i].repeatType == 0)
                        && targetList[i].gameObject.activeInHierarchy == true && targetList[i].asleep == false)
                    {
                        if (targetList[i].daysOfWeek.Count == 0 || targetList[i].daysOfWeek.Contains(System.DateTime.Today.DayOfWeek))
                        {
                            MakeHabit(i);
                        }
                    }
                }
                else
                {
                    if ((targetList[i].repeatType == repeatType || repeatType == 0)   // If the repeatTypes match, or if repeatType == 0 (which means it shows everything)
                        && targetList[i].gameObject.activeInHierarchy == true && targetList[i].asleep == false && (targetList[i].repeatType == 0 || targetList[i].done == false))
                    {
                        MakeHabit(i);
                    }
                }
            }
        }
    }

    public void MakeHabit(int i)
    {
        HabitObject newHabitInstance = Instantiate(blankHabit) as HabitObject;
        newHabitInstance.myHabit = targetList[i];
        newHabitInstance.habitName = targetList[i].habitName;
        newHabitInstance.repeatType = targetList[i].repeatType;
        newHabitInstance.doItList = targetList[i].doItList;
        newHabitInstance.rewardPoints = targetList[i].rewardPoints;
        newHabitInstance.missedPoints = targetList[i].missedPoints;
        newHabitInstance.showPoints = targetList[i].showPoints;
        //public object rewardToken;
        //public object missedLoss;
        newHabitInstance.asleep = targetList[i].asleep;
        newHabitInstance.done = targetList[i].done;
        newHabitInstance.resetDate = targetList[i].resetDate;
        newHabitInstance.inARow = targetList[i].inARow;
        newHabitInstance.missed = targetList[i].missed;
        newHabitInstance.transform.SetParent(this.transform);
        newHabitInstance.GetComponent<RectTransform>().localScale = Vector3.one;
        newHabitInstance.Start();
        newHabitInstance.Resize();
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
        DrawTasks();
    }

    private void OnDisable()
    {
        Clear();
    }

    public void Edit(HabitObject habit)
    {
        editHabitWindow.habitToEdit = habit;
        editHabitWindow.gameObject.SetActive(true);
        saveHabitButton.gameObject.SetActive(true);
        editHabitWindow.PrepScreen();
    }
}
