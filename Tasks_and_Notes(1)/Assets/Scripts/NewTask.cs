using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Globalization;

public class NewTask : MonoBehaviour
{
    public TaskObject blankTask;
    public InputField taskName;
    public Dropdown taskFolderBox;
    public InputField dueDate;
    public Toggle optionalBttn;
    public int repeatType;
    public List<GameObject> children;
    public GameObject allUI;
    public TaskObject taskToEdit;   // This variable is set by the "edit" button in "MakeEditButtons"
    public InputField taskFolderName;
    public Dropdown priorityBox;
    public List<String> userTags;
    public InputField tagsInput;
    public Dropdown repeatTypeInput;
    //public InputField rewardToken;
    //public InputField missedLoss;

    public void ClearEdit()
    {
        taskToEdit = null;
    }

    private void OnEnable()
    {
        PrepScreen();
    }

    public void SetRepeatType(int number)
    {
        repeatType = number;
    }

    public void PrepScreen()
    {
        taskFolderBox.ClearOptions();

        taskFolderBox.AddOptions(AppControl.control.taskFoldersList);

        try
        {
            taskName.text = taskToEdit.taskName;

            dueDate.text = Convert.ToString(taskToEdit.dueDate);
            optionalBttn.isOn = taskToEdit.optional;
            //rewardPoints.text = Convert.ToString(taskToEdit.rewardPoints);
            //missedPoints.text = Convert.ToString(taskToEdit.missedPoints);
            priorityBox.value = taskToEdit.priority;

            repeatTypeInput.value = repeatType;
            

            taskFolderBox.value = AppControl.control.taskFoldersList.IndexOf(taskToEdit.taskFolder);

            tagsInput.text = "";
            foreach(string tag in taskToEdit.userTags)
            {
                if (tagsInput.text == "")
                {
                    tagsInput.text = tag;
                }
                else
                {
                    tagsInput.text = tagsInput.text + ", " + tag;
                }
            }
        }
        catch (Exception) //e)
        {
            //Debug.LogException(e, this);

            taskName.text = "";
            dueDate.text = "";
            //rewardPoints.text = "0";
            //missedPoints.text = "0";
            taskName.ActivateInputField();
            priorityBox.value = 4;
            tagsInput.text = "";
            repeatTypeInput.value = 1;
        }
    }

    public void IsOptional()
    {
        optionalBttn.isOn = true;
    }

    public void IsNotOptional()
    {
        optionalBttn.isOn = false;
    }

    public void NewTaskFolder()
    {
        AppControl.control.taskFoldersList.Add(CultureInfo.CurrentCulture.TextInfo.ToTitleCase(taskFolderName.text.ToLower()));

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }

        taskFolderBox.ClearOptions();

        taskFolderBox.AddOptions(AppControl.control.taskFoldersList);

        taskFolderBox.value = AppControl.control.taskFoldersList.IndexOf(CultureInfo.CurrentCulture.TextInfo.ToTitleCase(taskFolderName.text.ToLower()));
    }

    public void Create()
    {
        if (taskName.text.Trim() != "")
        {
            TaskObject newTaskInstance = Instantiate(blankTask) as TaskObject;

            newTaskInstance.taskName = taskName.text.Trim();
            newTaskInstance.taskFolder = taskFolderBox.options[taskFolderBox.value].text;

            if (dueDate.text.ToLower().Contains("now"))
            {
                newTaskInstance.dueDate = System.DateTime.Now;
            }
            else if (dueDate.text.ToLower().Contains("tod"))
            {
                newTaskInstance.dueDate = System.DateTime.Today;
            }
            else if (dueDate.text.ToLower().Contains("tom"))
            {
                newTaskInstance.dueDate = System.DateTime.Today.AddDays(1);
            }
            else if (dueDate.text != "" && dueDate.text != null)
            {
                try
                {
                    newTaskInstance.dueDate = Convert.ToDateTime(dueDate.text);
                }
                catch (Exception) //e)
                {
                    //Debug.LogException(e, this);

                    print("Date not recognized");
                    newTaskInstance.dueDate = Convert.ToDateTime("1/1/0001");
                }
            }
            newTaskInstance.optional = optionalBttn.isOn;
            newTaskInstance.repeatType = repeatTypeInput.value;
            newTaskInstance.priority = priorityBox.value;

            string[] tempList = tagsInput.text.Split(',');
            foreach (string tag in tempList)
            {
                
                if (tag.Trim() != "" && newTaskInstance.userTags.Contains(tag.Trim().ToLower()) == false)
                {
                    newTaskInstance.userTags.Add(tag.Trim().ToLower());
                } 
            }

            AppControl.control.tasksList.Add(newTaskInstance);
            allUI.SetActive(false);
            allUI.SetActive(true);

            if (AppControl.control.autosave)
            {
                AppControl.control.Save();
            }
        }
        else
        {
            print("Cannot save a task with no name.");
        }
    }


    public void SaveEdit()
    {
        if (taskName.text.Trim() != "")
        {
            AppControl.control.tasksList.Remove(taskToEdit);

            this.taskToEdit.taskName = taskName.text.Trim();

            this.taskToEdit.taskFolder = taskFolderBox.options[taskFolderBox.value].text;

            if (dueDate.text.ToLower().Contains("now"))
            {
                taskToEdit.dueDate = System.DateTime.Now;
            }
            else if (dueDate.text.ToLower().Contains("tod"))
            {
                taskToEdit.dueDate = System.DateTime.Today;
            }
            else if (dueDate.text.ToLower().Contains("tom"))
            {
                taskToEdit.dueDate = System.DateTime.Today.AddDays(1);
            }
            else if (dueDate.text != "" && dueDate.text != null)
            {
                try
                {
                    taskToEdit.dueDate = Convert.ToDateTime(dueDate.text);
                }
                catch (Exception) //e)
                {
                    //Debug.LogException(e, this);

                    print("Date not recognized");
                    taskToEdit.dueDate = Convert.ToDateTime("1/1/0001");
                }
            }

            taskToEdit.repeatType = repeatTypeInput.value;
            taskToEdit.optional = optionalBttn.isOn;
            taskToEdit.priority = priorityBox.value;

            taskToEdit.userTags = new List<string>();
            string[] tempList = tagsInput.text.Split(',');
            foreach (string tag in tempList)
            {
                if (tag.Trim() != "" && taskToEdit.userTags.Contains(tag.Trim().ToLower()) == false)
                {
                    taskToEdit.userTags.Add(tag.Trim().ToLower());
                }
            }

            AppControl.control.tasksList.Add(taskToEdit);

            taskToEdit = null;

            allUI.SetActive(false);
            allUI.SetActive(true);

            if (AppControl.control.autosave)
            {
                AppControl.control.Save();
            }
        }
        else
        {
            print("Cannot save a task with no name.");
        }
    }
}
