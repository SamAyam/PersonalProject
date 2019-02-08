using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Globalization;

public class ChangeTaskDate : MonoBehaviour
{
    public InputField dueDate;
    public GameObject allUI;
    public TaskButtonsScript buttonClickedScript;

    private void OnEnable()
    {
        PrepScreen();
    }

    public void PrepScreen()
    {
        try
        {
            if (buttonClickedScript.selectedList[0].dueDate == Convert.ToDateTime("1/1/0001"))
            {
                dueDate.text = "";
            }
            else
            {
                dueDate.text = Convert.ToString(buttonClickedScript.selectedList[0].dueDate);
            }
        }
        catch (Exception) //e)
        {
            //Debug.LogException(e, this);
            dueDate.text = "";
        }
        dueDate.ActivateInputField();
    }
    

    public void ChangeDate()
    {
        foreach (TaskObject taskToEdit in buttonClickedScript.selectedList)
        {
            if (dueDate.text.ToLower().Contains("now"))
            {
                taskToEdit.myTask.dueDate = System.DateTime.Now;
            }
            else if (dueDate.text.ToLower().Contains("tod"))
            {
                taskToEdit.myTask.dueDate = System.DateTime.Today;
            }
            else if (dueDate.text.ToLower().Contains("tom"))
            {
                taskToEdit.myTask.dueDate = System.DateTime.Today.AddDays(1);
            }
            else if (dueDate.text != "" && dueDate.text != null)
            {
                try
                {
                    taskToEdit.myTask.dueDate = Convert.ToDateTime(dueDate.text);
                }
                catch (Exception) //e)
                {
                    //Debug.LogException(e, this);
                    print("Date not recognized");
                    taskToEdit.myTask.dueDate = Convert.ToDateTime("1/1/0001");
                }
            }
        }
        buttonClickedScript.selectedList = new List<TaskObject>();

        buttonClickedScript = null;

        allUI.SetActive(false);
        allUI.SetActive(true);

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }
    }

    public void ClearButtonClickedScript()
    {
        buttonClickedScript = null;
    }
}