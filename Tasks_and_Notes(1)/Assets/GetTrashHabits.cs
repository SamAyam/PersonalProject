using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetTrashHabits : MonoBehaviour
{
    public HabitObject blankHabit;

    public void DrawHabits()
    {
        if (AppControl.control != null)
        {
            Clear();
            for (int i = 0; i < AppControl.control.habitsTrashList.Count; i++)
            {
                HabitObject newHabitInstance = Instantiate(blankHabit) as HabitObject;

                newHabitInstance.myHabit = AppControl.control.habitsTrashList[i];
                newHabitInstance.habitName = AppControl.control.habitsTrashList[i].habitName;
                newHabitInstance.repeatType = AppControl.control.habitsTrashList[i].repeatType;
                newHabitInstance.doItList = AppControl.control.habitsTrashList[i].doItList;
                newHabitInstance.rewardPoints = AppControl.control.habitsTrashList[i].rewardPoints;
                newHabitInstance.missedPoints = AppControl.control.habitsTrashList[i].missedPoints;
                //newHabitInstance.rewardToken = AppControl.control.habitsTrashList[i].rewardToken;
                //newHabitInstance.missedLoss = AppControl.control.habitsTrashList[i].missedLoss;
                newHabitInstance.showPoints = AppControl.control.habitsTrashList[i].showPoints;
                newHabitInstance.asleep = AppControl.control.habitsTrashList[i].asleep;
                newHabitInstance.done = AppControl.control.habitsTrashList[i].done;
                newHabitInstance.resetDate = AppControl.control.habitsTrashList[i].resetDate;
                newHabitInstance.inARow = AppControl.control.habitsTrashList[i].inARow;
                newHabitInstance.missed = AppControl.control.habitsTrashList[i].missed;
                newHabitInstance.transform.SetParent(this.transform);
                newHabitInstance.GetComponent<RectTransform>().localScale = Vector3.one;
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

