using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetDoneHabits : MonoBehaviour
{
    public HabitObject blankHabit;

    public void DrawHabits()
    {
        if (AppControl.control != null)
        {
            Clear();
            for (int i = 0; i < AppControl.control.habitsList.Count; i++)
            {
                if (AppControl.control.habitsList[i].done == true && AppControl.control.habitsList[i].asleep == false)
                {
                    HabitObject newHabitInstance = Instantiate(blankHabit) as HabitObject;

                    newHabitInstance.myHabit = AppControl.control.habitsList[i];
                    newHabitInstance.habitName = AppControl.control.habitsList[i].habitName;
                    newHabitInstance.repeatType = AppControl.control.habitsList[i].repeatType;
                    newHabitInstance.doItList = AppControl.control.habitsList[i].doItList;
                    newHabitInstance.rewardPoints = AppControl.control.habitsList[i].rewardPoints;
                    newHabitInstance.missedPoints = AppControl.control.habitsList[i].missedPoints;
                    //newHabitInstance.rewardToken = AppControl.control.habitsList[i].rewardToken;
                    //newHabitInstance.missedLoss = AppControl.control.habitsList[i].missedLoss;
                    newHabitInstance.showPoints = AppControl.control.habitsList[i].showPoints;
                    newHabitInstance.asleep = AppControl.control.habitsList[i].asleep;
                    newHabitInstance.done = AppControl.control.habitsList[i].done;
                    newHabitInstance.resetDate = AppControl.control.habitsList[i].resetDate;
                    newHabitInstance.inARow = AppControl.control.habitsList[i].inARow;
                    newHabitInstance.missed = AppControl.control.habitsList[i].missed;
                    newHabitInstance.transform.SetParent(this.transform);
                    newHabitInstance.GetComponent<RectTransform>().localScale = Vector3.one;
                }

            }
        }
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
        DrawHabits();
    }

    private void OnDisable()
    {
        Clear();
    }
}

