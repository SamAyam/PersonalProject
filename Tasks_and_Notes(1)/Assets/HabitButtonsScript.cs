using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

public class HabitButtonsScript : MonoBehaviour
{
    public Button daysOfWeekB;  
    public Button editB;
    public Button commentsB;
    public Button remindersB;
    public Button doneB;
    public NewHabitScript editHabitWindow;
    public GameObject saveHabitButton;
    public List<HabitObject> selectedList = new List<HabitObject>();
    public GameObject singleSelectedPanel;
    public GameObject multipleSelectedPanel;
    public GameObject topButtonsPanel;
    //public ChangeTaskDate changeDateScreen;
    public Button tagsB;
    public Button priorityB;
    public Button folderB;
    public Button multDaysOfWeekB; 
    public Button multDoneB;
    //public AddCommentToTask commentsWindow;
    //public GetComments getComments;
    public GameObject priorityScreen;
    public GameObject userTagsScreen;
    public ChangeTaskFolder changeFolderScreen;
    
    public GetHabits getHabitScript;



    private void Awake()
    {
        remindersB.onClick.AddListener(delegate { RemindersB(); });
        commentsB.onClick.AddListener(delegate { CommentsB(); });
        editB.onClick.AddListener(delegate { EditB(); });
        daysOfWeekB.onClick.AddListener(delegate { DaysOfWeekB(); });
        doneB.onClick.AddListener(delegate { DoneB(); });

        tagsB.onClick.AddListener(delegate { TagsB(); });
        priorityB.onClick.AddListener(delegate { PriorityB(); });
        folderB.onClick.AddListener(delegate { FolderB(); });
        multDaysOfWeekB.onClick.AddListener(delegate { DaysOfWeekB(); });
        multDoneB.onClick.AddListener(delegate { MultDoneB(); });
    }


    private void Update()
    {
        if (selectedList.Count == 1)
        {
            topButtonsPanel.SetActive(true);
            singleSelectedPanel.SetActive(true);
            multipleSelectedPanel.SetActive(false);
        }
        else if (selectedList.Count > 1)
        {
            topButtonsPanel.SetActive(true);
            singleSelectedPanel.SetActive(false);
            multipleSelectedPanel.SetActive(true);
        }
        else
        {
            topButtonsPanel.SetActive(false);
            singleSelectedPanel.SetActive(false);
            multipleSelectedPanel.SetActive(false);
        }
    }

    private void TagsB()
    {
        print("TagsB");
        //    userTagsScreen.GetComponent<ChangeTaskTag>().buttonClickedScript = this;
        //    userTagsScreen.SetActive(true);
    }

    private void PriorityB()
    {
        print("PriorityB");
        //    priorityScreen.GetComponent<ChangeTaskPriority>().buttonClickedScript = this;
        //    priorityScreen.gameObject.SetActive(true);
    }

    private void FolderB()
    {
        print("FolderB");
        //    changeFolderScreen.buttonClickedScript = this;
        //    changeFolderScreen.PrepScreen();
        //    changeFolderScreen.gameObject.SetActive(true);
    }

    private void RemindersB()
    {
        print("TODO: Reminders");
    }

    private void CommentsB()
    {
        print("CommentsB");
        //    getComments.task = selectedList[0].myTask;
        //    commentsWindow.taskToEdit = selectedList[0].myTask;
        //    commentsWindow.gameObject.SetActive(true);
        //    commentsWindow.PrepScreen();
    }

    private void EditB()
    {
        getHabitScript.Edit(selectedList[0].myHabit);
        //this.transform.parent.parent.parent.GetComponent<GetHabits>().Edit(this.transform.parent.parent.GetComponent<HabitObject>().myHabit);
        //editHabitWindow.habitToEdit = selectedList[0].myHabit;
        //editHabitWindow.gameObject.SetActive(true);
        //saveHabitButton.gameObject.SetActive(true);
        //editHabitWindow.PrepScreen();
    }

    private void DaysOfWeekB()
    {
        print("DaysOfWeekB");
        //    changeDateScreen.buttonClickedScript = this;
        //    changeDateScreen.gameObject.SetActive(true);
    }

    private void DoneB()
    {
        //print("DoneB");
        //AppControl.control.donesList.Add(selectedList[0].myTask);
        //AppControl.control.tasksList.Remove(selectedList[0].myTask);
        //Destroy(selectedList[0].gameObject);
        //selectedList = new List<TaskObject>();

        //if (AppControl.control.autosave)
        //{
        //    AppControl.control.Save();
        //}
        HabitObject habit = selectedList[0].myHabit;
        if (habit.repeatType != 0)
        {
            habit.done = true;
            if (habit.missed)
            {
                habit.missed = false;
                habit.inARow = 1;
                habit.redCircle.SetActive(false);
                habit.yellowCircle.SetActive(false);
                habit.blueCircle.SetActive(true);
            }
            else
            {
                habit.inARow += 1;
            }

            if (habit.repeatType == 1)
            {
                habit.resetDate = System.DateTime.Today.AddDays(1);
            }
            else if (habit.repeatType == 2)
            {
                habit.resetDate = DateTime.Today.AddDays(7 - Convert.ToInt16(DateTime.Today.DayOfWeek));
            }
            else if (habit.repeatType == 3)
            {
                habit.resetDate = System.DateTime.Today.AddDays(1 - DateTime.Today.Day).AddMonths(1);
            }
            else if (habit.repeatType == 4)
            {
                habit.resetDate = Convert.ToDateTime("1/1/0001").AddYears(DateTime.Today.Year);
            }
            else
            {
                habit.resetDate = Convert.ToDateTime("1/1/0001");
            }
            Destroy(habit.gameObject);
        }
        else
        {
            habit.done = true;
            if (habit.missed)
            {
                habit.missed = false;
                habit.inARow = 1;
                habit.redCircle.SetActive(false);
                habit.yellowCircle.SetActive(false);
                habit.blueCircle.SetActive(true);
            }
            else
            {
                habit.inARow += 1;
            }
            habit.resetDate = System.DateTime.Today.AddDays(1);
            //transform.parent.parent.parent.GetComponent<GetHabits>().DrawTasks();
            getHabitScript.DrawTasks();
        }
        //print(habit.resetDate);
        print("addPoints() goes here"); //??????

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }
    }

    private void MultDoneB()
    {
        print("MultDoneB");
        //List<HabitObject> deleteList = new List<HabitObject>();
        //foreach (HabitObject habit in selectedList)
        //{
        //    habit.myHabit.done = true;
        //    AppControl.control.habitd.Add(habit.myHabit);
        //    AppControl.control.tasksList.Remove(habit.myHabit);
        //    deleteList.Add(task);
        //}
        //foreach (TaskObject task in deleteList)
        //{
        //    Destroy(task.gameObject);
        //}
        //selectedList = new List<TaskObject>();

        //if (AppControl.control.autosave)
        //{
        //    AppControl.control.Save();
        //}
    }
}