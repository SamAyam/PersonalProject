using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetTrash : MonoBehaviour
{
    //public Transform parentWindow;
    public TaskObject blankTask;

    public void DrawTasks()
    {
        if (AppControl.control != null)
        {
            Clear();
            //AppControl.control.tasksList.Sort((p1, p2) => p1.dueDate.CompareTo(p2.dueDate));
            for (int i = 0; i < AppControl.control.trashList.Count; i++)
            {
                TaskObject newTaskInstance = Instantiate(blankTask) as TaskObject;
                newTaskInstance.myTask = AppControl.control.trashList[i];
                newTaskInstance.taskFolder = AppControl.control.trashList[i].taskFolder;
                newTaskInstance.taskName = AppControl.control.trashList[i].taskName;
                newTaskInstance.dueDate = AppControl.control.trashList[i].dueDate;
                newTaskInstance.optional = AppControl.control.trashList[i].optional;
                newTaskInstance.repeatType = AppControl.control.trashList[i].repeatType;
                newTaskInstance.transform.SetParent(this.transform);
                newTaskInstance.GetComponent<RectTransform>().localScale = Vector3.one;
            }
        }
    }

    public void Clear()
    {
        //while (GameObject.FindWithTag("DeleteOnLoad") != null) Destroy(GameObject.FindWithTag("DeleteOnLoad"));
        foreach (Transform child in transform)
        {
            GameObject.Destroy(child.gameObject);
        }
    }

    private void OnEnable()
    {
        DrawTasks();
    }

    private void OnDisable()
    {
        Clear();
    }
}

