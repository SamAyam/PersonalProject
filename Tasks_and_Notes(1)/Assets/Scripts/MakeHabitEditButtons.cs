using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

public class MakeHabitEditButtons : MonoBehaviour
{
    public Button editButton;
    Button editB;
    public Button sleepButton;
    Button sleepB;
    public Button cancelButton;
    Button cancelB;
    public Button doneButton;
    Button doneB;
    




    private void Awake()
    {
        editB = Instantiate(editButton) as Button;
        editB.transform.SetParent(transform);
        editB.GetComponent<RectTransform>().localScale = Vector3.one;
        editB.onClick.AddListener(delegate { EditB(); });
        sleepB = Instantiate(sleepButton) as Button;
        sleepB.transform.SetParent(transform);
        sleepB.GetComponent<RectTransform>().localScale = Vector3.one;
        sleepB.onClick.AddListener(delegate { SleepB(); });
        cancelB = Instantiate(cancelButton) as Button;
        cancelB.transform.SetParent(transform);
        cancelB.GetComponent<RectTransform>().localScale = Vector3.one;
        cancelB.onClick.AddListener(delegate { CancelB(); });
        doneB = Instantiate(doneButton) as Button;
        doneB.transform.SetParent(transform);
        doneB.GetComponent<RectTransform>().localScale = Vector3.one;
        doneB.onClick.AddListener(delegate { DoneB(); });
    }

    private void EditB()
    {
        this.transform.parent.parent.parent.GetComponent<GetHabits>().Edit(this.transform.parent.parent.GetComponent<HabitObject>().myHabit);
        
        
        //if (AppControl.control.snapsList.Contains(transform.parent.parent.GetComponent<HabitObject>().myHabit))
        //{
        //    editSnapWindow.habitToEdit = this.transform.parent.GetComponent<HabitObject>().myHabit;
        //    editSnapWindow.gameObject.SetActive(true);
        //    saveSnapButton.gameObject.SetActive(true);
        //    editSnapWindow.PrepScreen();
        //}
        //else
        //{
        //    editHabitWindow.habitToEdit = this.transform.parent.GetComponent<HabitObject>().myHabit;
        //    editHabitWindow.gameObject.SetActive(true);
        //    saveHabitButton.gameObject.SetActive(true);
        //    editHabitWindow.PrepScreen();
        //}
    }

    private void SleepB()
    {
        if (this.transform.parent.parent.GetComponent<HabitObject>().myHabit.asleep == true)
        {
            this.transform.parent.parent.GetComponent<HabitObject>().myHabit.asleep = false;
            Destroy(this.transform.parent.parent.gameObject);
        }
        else
        {
            this.transform.parent.parent.GetComponent<HabitObject>().myHabit.asleep = true;
            Destroy(this.transform.parent.parent.gameObject);
        }

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }
    }

    private void DeleteB() // Not in use, move to "sleepScreen"
    {
        AppControl.control.habitsTrashList.Add(transform.parent.parent.GetComponent<HabitObject>().myHabit);
        AppControl.control.habitsList.Remove(transform.parent.parent.GetComponent<HabitObject>().myHabit);
        AppControl.control.snapsList.Remove(transform.parent.parent.GetComponent<HabitObject>().myHabit);
        
        Destroy(this.transform.parent.parent.gameObject);

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }

        //TODO: punishments? deduct points?
        //this.transform.parent.gameObject.SetActive(false);
    }

    private void CancelB()
    {
        this.gameObject.SetActive(false);
    }

    private void DoneB()
    {
        if (this.transform.parent.parent.GetComponent<HabitObject>().myHabit.repeatType !=0)
        {
            this.transform.parent.parent.GetComponent<HabitObject>().myHabit.done = true;
            if (transform.parent.parent.GetComponent<HabitObject>().myHabit.missed)
            {
                transform.parent.parent.GetComponent<HabitObject>().myHabit.missed = false;
                transform.parent.parent.GetComponent<HabitObject>().myHabit.inARow = 1;
                transform.parent.parent.GetComponent<HabitObject>().myHabit.redCircle.SetActive(false);
                transform.parent.parent.GetComponent<HabitObject>().myHabit.yellowCircle.SetActive(false);
                transform.parent.parent.GetComponent<HabitObject>().myHabit.blueCircle.SetActive(true);
            }
            else
            {
                transform.parent.parent.GetComponent<HabitObject>().myHabit.inARow += 1;
            }

            if (this.transform.parent.parent.GetComponent<HabitObject>().myHabit.repeatType == 1)
            {
                this.transform.parent.parent.GetComponent<HabitObject>().myHabit.resetDate = System.DateTime.Today.AddDays(1);
            }
            else if (this.transform.parent.parent.GetComponent<HabitObject>().myHabit.repeatType == 2)
            {
                this.transform.parent.parent.GetComponent<HabitObject>().myHabit.resetDate = DateTime.Today.AddDays(7 - Convert.ToInt16(DateTime.Today.DayOfWeek));
            }
            else if (this.transform.parent.parent.GetComponent<HabitObject>().myHabit.repeatType == 3)
            {
                this.transform.parent.parent.GetComponent<HabitObject>().myHabit.resetDate = System.DateTime.Today.AddDays(1 - DateTime.Today.Day).AddMonths(1);
            }
            else if (this.transform.parent.parent.GetComponent<HabitObject>().myHabit.repeatType == 4)
            {
                this.transform.parent.parent.GetComponent<HabitObject>().myHabit.resetDate = Convert.ToDateTime("1/1/0001").AddYears(DateTime.Today.Year);
            }
            else
            {
                this.transform.parent.parent.GetComponent<HabitObject>().myHabit.resetDate = Convert.ToDateTime("1/1/0001");
            }
            Destroy(this.transform.parent.parent.gameObject);
        }
        else
        {
            this.transform.parent.parent.GetComponent<HabitObject>().myHabit.done = true;
            if (transform.parent.parent.GetComponent<HabitObject>().myHabit.missed)
            {
                transform.parent.parent.GetComponent<HabitObject>().myHabit.missed = false;
                transform.parent.parent.GetComponent<HabitObject>().myHabit.inARow = 1;
                transform.parent.parent.GetComponent<HabitObject>().myHabit.redCircle.SetActive(false);
                transform.parent.parent.GetComponent<HabitObject>().myHabit.yellowCircle.SetActive(false);
                transform.parent.parent.GetComponent<HabitObject>().myHabit.blueCircle.SetActive(true);
            }
            else
            {
                transform.parent.parent.GetComponent<HabitObject>().myHabit.inARow += 1;
            }
            this.transform.parent.parent.GetComponent<HabitObject>().myHabit.resetDate = System.DateTime.Today.AddDays(1);
            transform.parent.parent.parent.GetComponent<GetHabits>().DrawTasks();
        }
        print(this.transform.parent.parent.GetComponent<HabitObject>().myHabit.resetDate);
        print("addPoints() goes here"); //??????

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }
    }
}
