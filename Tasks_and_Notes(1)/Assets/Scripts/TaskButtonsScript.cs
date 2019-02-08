using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TaskButtonsScript : MonoBehaviour
{
    public Button dueDateB;
    public Button editB;
    public Button commentsB;
    public Button remindersB;
    public Button doneB;
    public NewTask editTaskWindow;
    public GameObject saveTaskButton;
    public List<TaskObject> selectedList = new List<TaskObject>();
    public GameObject singleSelectedPanel;
    public GameObject multipleSelectedPanel;
    public GameObject topButtonsPanel;
    public ChangeTaskDate changeDateScreen;
    public Button tagsB;
    public Button priorityB;
    public Button folderB;
    public Button multDueDateB;
    public Button multDoneB;
    public AddCommentToTask commentsWindow;
    public GetComments getComments;
    public GameObject priorityScreen;
    public GameObject userTagsScreen;
    public ChangeTaskFolder changeFolderScreen;



    private void Awake()
    {
        remindersB.onClick.AddListener(delegate { RemindersB(); });
        commentsB.onClick.AddListener(delegate { CommentsB(); });
        editB.onClick.AddListener(delegate { EditB(); });
        dueDateB.onClick.AddListener(delegate { DueDateB(); });
        doneB.onClick.AddListener(delegate { DoneB(); });

        tagsB.onClick.AddListener(delegate { TagsB(); });
        priorityB.onClick.AddListener(delegate { PriorityB(); });
        folderB.onClick.AddListener(delegate { FolderB(); });
        multDueDateB.onClick.AddListener(delegate { DueDateB(); });
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
        userTagsScreen.GetComponent<ChangeTaskTag>().buttonClickedScript = this;
        userTagsScreen.SetActive(true);
    }

    private void PriorityB()
    {
        priorityScreen.GetComponent<ChangeTaskPriority>().buttonClickedScript = this;
        priorityScreen.gameObject.SetActive(true);
    }

    private void FolderB()
    {
        changeFolderScreen.buttonClickedScript = this;
        changeFolderScreen.PrepScreen();
        changeFolderScreen.gameObject.SetActive(true);
    }

    private void RemindersB()
    {
        print("TODO: Reminders");
    }

    private void CommentsB()
    {
        getComments.task = selectedList[0].myTask;
        commentsWindow.taskToEdit = selectedList[0].myTask;
        commentsWindow.gameObject.SetActive(true);
        commentsWindow.PrepScreen();
    }

    private void EditB()
    {
        editTaskWindow.taskToEdit = selectedList[0].myTask;
        editTaskWindow.gameObject.SetActive(true);
        saveTaskButton.gameObject.SetActive(true);
        editTaskWindow.PrepScreen();
    }

    private void DueDateB()
    {
        changeDateScreen.buttonClickedScript = this;
        changeDateScreen.gameObject.SetActive(true);
    }

    private void DoneB()
    {
        AppControl.control.donesList.Add(selectedList[0].myTask);
        AppControl.control.tasksList.Remove(selectedList[0].myTask);
        Destroy(selectedList[0].gameObject);
        selectedList = new List<TaskObject>();

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }
    }

    private void MultDoneB()
    {
        List<TaskObject> deleteList = new List<TaskObject>();
        foreach (TaskObject task in selectedList)
        {
            AppControl.control.donesList.Add(task.myTask);
            AppControl.control.tasksList.Remove(task.myTask);
            deleteList.Add(task);
        }
        foreach(TaskObject task in deleteList)
        { 
            Destroy(task.gameObject);
        }
        selectedList = new List<TaskObject>();

        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }
    }
}