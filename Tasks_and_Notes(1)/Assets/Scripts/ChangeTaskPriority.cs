using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Globalization;

public class ChangeTaskPriority : MonoBehaviour
{
    //public Transform parentWindow;
    public Dropdown priorityBox;
    public GameObject allUI;
    public TaskButtonsScript buttonClickedScript;

    public void PrepScreen()
    {
        priorityBox.value = 0;
    }


    public void ChangePriority()
    {
        foreach (TaskObject taskToEdit in buttonClickedScript.selectedList)
        {
            //AppControl.control.tasksList.Remove(taskToEdit.myTask);

            taskToEdit.myTask.priority = priorityBox.value;

            //AppControl.control.tasksList.Add(taskToEdit.myTask);
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
