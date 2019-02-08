using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TopTaskButtons : MonoBehaviour { 
    public Button backB;
    public Button deleteB;
    public TaskButtonsScript bottomBScript;
    public GameObject optionsPanel;
    public GameObject allUI;

    
    private void Awake()
    {
        
        backB.onClick.AddListener(delegate { BackB(); });
        deleteB.onClick.AddListener(delegate { DeleteB(); });
    }

    private void OnDisable()
    {
        optionsPanel.SetActive(false);
    }

    private void BackB()
    {
        List<GameObject> deleteList = new List<GameObject>();
        foreach(TaskObject task in bottomBScript.selectedList)
        {
            deleteList.Add(task.transform.Find("TaskClickedPanel").gameObject);
        }
        foreach (GameObject task in deleteList)
        { 
            task.SetActive(false);
        }
        bottomBScript.selectedList = new List<TaskObject>();
    }

    private void DeleteB()
    {
        //TODO: punishments? deduct points?
        //this.transform.parent.gameObject.SetActive(false);
        foreach (TaskObject task in bottomBScript.selectedList)
        {
            AppControl.control.trashList.Add(task.myTask);
            AppControl.control.tasksList.Remove(task.myTask);
        }
        
        bottomBScript.selectedList = new List<TaskObject>();
        allUI.SetActive(false);
        allUI.SetActive(true);


    }
}