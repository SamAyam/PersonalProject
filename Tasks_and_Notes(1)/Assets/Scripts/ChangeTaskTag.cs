using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Globalization;

public class ChangeTaskTag : MonoBehaviour
{
    public InputField userTagsInput;
    public GameObject allUI;
    public TaskButtonsScript buttonClickedScript;

    private void OnEnable()
    {
        PrepScreen();
    }

    public void PrepScreen()
    {
        userTagsInput.text = "";
        userTagsInput.ActivateInputField();
    }
    
    public void AddTags()
    {
        foreach (TaskObject taskToEdit in buttonClickedScript.selectedList)
        {
            string[] tempList = userTagsInput.text.Split(',');
            foreach (string tag in tempList)
            {
                if (tag.Trim() != "" && taskToEdit.userTags.Contains(tag.Trim().ToLower()) == false)
                {
                    taskToEdit.userTags.Add(tag.Trim().ToLower());
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
