using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Globalization;

public class ChangeTaskFolder : MonoBehaviour {

    //public Transform parentWindow;
    public Dropdown FolderBox;
    public GameObject allUI;
    public TaskButtonsScript buttonClickedScript;

    public void PrepScreen()
    {
        FolderBox.ClearOptions();
        FolderBox.AddOptions(AppControl.control.taskFoldersList);
        FolderBox.value = 0;
    }


    public void ChangeFolder()
    {
        foreach (TaskObject taskToEdit in buttonClickedScript.selectedList)
        {
            taskToEdit.myTask.taskFolder = FolderBox.options[FolderBox.value].text;
            //taskToEdit.myTask.taskFolder = Convert.ToString(FolderBox.options[FolderBox.value]);
            print(taskToEdit.myTask.taskFolder);
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
