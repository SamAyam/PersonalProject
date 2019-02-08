using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

public class NewHabitScript : MonoBehaviour
{
    public HabitObject blankHabit;
    public int repeatType;
    public InputField habitName;
    public InputField rewardPoints;
    public InputField missedPoints;
    //public InputField rewardToken;
    //public InputField missedLoss;
    public Toggle showPointsBttn;
    public Button doItButton;
    public DoItObject blankDoIt;
    public List<DoItObject> doItList = new List<DoItObject>();
    public List<GameObject> children;
    public GameObject allUI;
    public Dropdown doItName;
    public InputField howToDoIt;
    public Toggle goodHabitButton;
    public HabitObject habitToEdit;   // This variable is set by the "edit" button in "MakeHabitEditButtons"
    public Dropdown repeatTypeInput;

    public Toggle sun;
    public Toggle mon;
    public Toggle tue;
    public Toggle wed;
    public Toggle thu;
    public Toggle fri;
    public Toggle sat;


    public void ClearEdit()
    {
        habitToEdit = null;
    }
    
    private void OnEnable()
    {
        PrepScreen();
    }

    public void PrepScreen()
    {
        try
        {
            habitName.text = habitToEdit.habitName;
            rewardPoints.text = Convert.ToString(habitToEdit.rewardPoints);
            missedPoints.text = Convert.ToString(habitToEdit.missedPoints);
            doItList = habitToEdit.doItList;
            showPointsBttn.isOn = habitToEdit.showPoints;
            repeatTypeInput.value = habitToEdit.repeatType;


            goodHabitButton.isOn = AppControl.control.habitsList.Contains(habitToEdit);

            if (habitToEdit.daysOfWeek.Contains(DayOfWeek.Sunday)) { sun.isOn = true; }
            else { sun.isOn = false; }
            if (habitToEdit.daysOfWeek.Contains(DayOfWeek.Monday)) { mon.isOn = true; }
            else { mon.isOn = false; }
            if (habitToEdit.daysOfWeek.Contains(DayOfWeek.Tuesday)) { tue.isOn = true; }
            else { tue.isOn = false; }
            if (habitToEdit.daysOfWeek.Contains(DayOfWeek.Wednesday)) { wed.isOn = true; }
            else { wed.isOn = false; }
            if (habitToEdit.daysOfWeek.Contains(DayOfWeek.Thursday)) { thu.isOn = true; }
            else { thu.isOn = false; }
            if (habitToEdit.daysOfWeek.Contains(DayOfWeek.Friday)) { fri.isOn = true; }
            else { fri.isOn = false; }
            if (habitToEdit.daysOfWeek.Contains(DayOfWeek.Saturday)) { sat.isOn = true; }
            else { sat.isOn = false; }
        }
        catch (Exception) //e)
        {
            //Debug.LogException(e, this);

            habitName.text = "";
            rewardPoints.text = "0";
            missedPoints.text = "0";
            doItList = new List<DoItObject>();
            habitName.ActivateInputField();
            repeatTypeInput.value = repeatType;

            sun.isOn = false;
            mon.isOn = false;
            tue.isOn = false;
            wed.isOn = false;
            thu.isOn = false;
            fri.isOn = false;
            sat.isOn = false;
        }
    }

    public void IsGoodHabit()
    {
        goodHabitButton.isOn = true;
    }

    public void IsBadHabit()
    {
        goodHabitButton.isOn = false;
    }

    public void ShowPoints()
    {
        showPointsBttn.isOn = true;
    }

    public void DoNotShowPoints()
    {
        showPointsBttn.isOn = false;
    }

    public void NewDoThis()
    {
        DoItObject newDoItInstance = Instantiate(blankDoIt) as DoItObject;
        if (doItName.value == 0)
        {
            newDoItInstance.doItName = "another habit";
        }
        newDoItInstance.howToDoIt = howToDoIt.text;
        doItList.Add(newDoItInstance);

        allUI.SetActive(false);
        allUI.SetActive(true);

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }
    }

    public void Create()
    {
        if (habitName.text.Trim() != "")
        {
            HabitObject newHabitInstance = Instantiate(blankHabit) as HabitObject;

            newHabitInstance.habitName = habitName.text.Trim();

            try
            {
                newHabitInstance.rewardPoints = Convert.ToInt32(rewardPoints.text);
            }
            catch (Exception) //e)
            {
                //Debug.LogException(e, this);

                print("Reward Points not recognized");
                newHabitInstance.rewardPoints = 0;
            }

            try
            {
                newHabitInstance.missedPoints = Convert.ToInt32(missedPoints.text);
            }
            catch (Exception) //e)
            {
                //Debug.LogException(e, this);

                print("Missed Points not recognized");
                newHabitInstance.rewardPoints = 0;
            }
            newHabitInstance.repeatType = repeatTypeInput.value;               // This can be "yearly", "monthly", "weekly", "daily", "" (constant)
            newHabitInstance.showPoints = showPointsBttn.isOn;
            newHabitInstance.doItList = doItList;


            if (sun.isOn == true) { newHabitInstance.daysOfWeek.Add(DayOfWeek.Sunday);}
            if (mon.isOn == true) { newHabitInstance.daysOfWeek.Add(DayOfWeek.Monday); }
            if (tue.isOn == true) { newHabitInstance.daysOfWeek.Add(DayOfWeek.Tuesday); }
            if (wed.isOn == true) { newHabitInstance.daysOfWeek.Add(DayOfWeek.Wednesday); }
            if (thu.isOn == true) { newHabitInstance.daysOfWeek.Add(DayOfWeek.Thursday); }
            if (fri.isOn == true) { newHabitInstance.daysOfWeek.Add(DayOfWeek.Friday); }
            if (sat.isOn == true) { newHabitInstance.daysOfWeek.Add(DayOfWeek.Saturday); }


            if (repeatTypeInput.value == 1 || repeatTypeInput.value ==0)  //Daily or constant
            {
                newHabitInstance.resetDate = DateTime.Today.AddDays(1);
            }
            else if (repeatTypeInput.value == 2)  //Weekly
            {
                newHabitInstance.resetDate = DateTime.Today.AddDays(7 - Convert.ToInt16(DateTime.Today.DayOfWeek));
            }
            else if (repeatTypeInput.value == 3)  //Monthly
            {
                newHabitInstance.resetDate = Convert.ToDateTime(Convert.ToString(DateTime.Today.AddMonths(1).Month) + "/1/" + Convert.ToString(DateTime.Today.Year));
            }
            else if (repeatTypeInput.value == 4)  //Yearly
            {
                newHabitInstance.resetDate = Convert.ToDateTime("1/1/" + Convert.ToString(DateTime.Today.AddYears(1).Year));
            }
            else  // error
            {
                newHabitInstance.resetDate = DateTime.Today;
            }
            print("ResetDate = " + Convert.ToString(newHabitInstance.resetDate));


            // The following is obsolete now that weeklies only check on sunday
            //if (newHabitInstance.daysOfWeek.Contains(DateTime.Today.DayOfWeek) == false && newHabitInstance.daysOfWeek.Count != 0) { newHabitInstance.done = true; }

            if (goodHabitButton.isOn)
            {
                AppControl.control.habitsList.Add(newHabitInstance);
            }
            else
            {
                AppControl.control.snapsList.Add(newHabitInstance);
            }
            allUI.SetActive(false);
            allUI.SetActive(true);

            if (AppControl.control.autosave)
            {
                AppControl.control.Save();
            }
        }
        else
        {
            print("Cannot save a habit with no name.");
        }
    }

    public void SaveEdit()
    {
        if (habitName.text.Trim() != "")
        {
            AppControl.control.snapsList.Remove(habitToEdit);
            AppControl.control.habitsList.Remove(habitToEdit);

            this.habitToEdit.habitName = habitName.text.Trim();

            try
            {
                habitToEdit.rewardPoints = Convert.ToInt32(rewardPoints.text);
            }
            catch (Exception) //e)
            {
                //Debug.LogException(e, this);

                print("Reward Points not recognized");
                habitToEdit.rewardPoints = 0;
            }

            try
            {
                habitToEdit.missedPoints = Convert.ToInt32(missedPoints.text);
            }
            catch (Exception) //e)
            {
                //Debug.LogException(e, this);

                print("Missed Points not recognized");
                habitToEdit.rewardPoints = 0;
            }
            habitToEdit.repeatType = repeatTypeInput.value;                 // This can be "yearly", "monthly", "weekly", "daily", "" (constant)
            habitToEdit.showPoints = showPointsBttn.isOn;
            habitToEdit.doItList = doItList;

            habitToEdit.daysOfWeek = new List<DayOfWeek>();
            if (sun.isOn == true) { habitToEdit.daysOfWeek.Add(DayOfWeek.Sunday); }
            if (mon.isOn == true) { habitToEdit.daysOfWeek.Add(DayOfWeek.Monday); }
            if (tue.isOn == true) { habitToEdit.daysOfWeek.Add(DayOfWeek.Tuesday); }
            if (wed.isOn == true) { habitToEdit.daysOfWeek.Add(DayOfWeek.Wednesday); }
            if (thu.isOn == true) { habitToEdit.daysOfWeek.Add(DayOfWeek.Thursday); }
            if (fri.isOn == true) { habitToEdit.daysOfWeek.Add(DayOfWeek.Friday); }
            if (sat.isOn == true) { habitToEdit.daysOfWeek.Add(DayOfWeek.Saturday); }

            if (repeatTypeInput.value == 1)  //Daily
            {
                habitToEdit.resetDate = DateTime.Today.AddDays(1);
            }
            else if (repeatTypeInput.value == 2)  //Weekly
            {
                habitToEdit.resetDate = DateTime.Today.AddDays(7 - Convert.ToInt16(DateTime.Today.DayOfWeek));
            }
            else if (repeatTypeInput.value == 3)  //Monthly
            {
                habitToEdit.resetDate = Convert.ToDateTime(Convert.ToString(DateTime.Today.AddMonths(1).Month) + "/1/" + Convert.ToString(DateTime.Today.Year));
            }
            else if (repeatTypeInput.value == 4)  //Yearly
            {
                habitToEdit.resetDate = Convert.ToDateTime("1/1/" + Convert.ToString(DateTime.Today.AddYears(1).Year));
            }
            else  // constant or error
            {
                habitToEdit.resetDate = DateTime.Today;
            }
            print("ResetDate = " + Convert.ToString(habitToEdit.resetDate));
            
            if (goodHabitButton.isOn == false)
            {
                AppControl.control.snapsList.Add(habitToEdit);
            }
            else
            {
                AppControl.control.habitsList.Add(habitToEdit);
            }
            allUI.SetActive(false);
            allUI.SetActive(true);

            habitToEdit = null;

            if (AppControl.control.autosave)
            {
                AppControl.control.Save();
            }
        }
        else
        {
            print("Cannot save a habit with no name.");
        }
    }

    public void SetRepeatType(int number)
    {
        repeatType = number;
    }
}
