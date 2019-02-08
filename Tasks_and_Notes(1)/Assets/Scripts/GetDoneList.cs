using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetDoneList : MonoBehaviour
{
    public TaskObject blankTask;

    public void DrawTasks()
    {
        if (AppControl.control != null)
        {
            Clear();

            //AppControl.control.tasksList.Sort((p1, p2) => p1.dueDate.CompareTo(p2.dueDate));

            for (int i = 0; i < AppControl.control.donesList.Count; i++)
            {
                TaskObject newTaskInstance = Instantiate(blankTask) as TaskObject;
                newTaskInstance.myTask = AppControl.control.donesList[i];
                newTaskInstance.taskFolder = AppControl.control.donesList[i].taskFolder;
                newTaskInstance.taskName = AppControl.control.donesList[i].taskName;
                newTaskInstance.dueDate = AppControl.control.donesList[i].dueDate;
                newTaskInstance.optional = AppControl.control.donesList[i].optional;
                newTaskInstance.repeatType = AppControl.control.donesList[i].repeatType;
                newTaskInstance.transform.SetParent(this.transform);
                newTaskInstance.GetComponent<RectTransform>().localScale = Vector3.one;

            }
        }
    }

    public void Clear()
    {
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
