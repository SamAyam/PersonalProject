using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TaskClickedScript : MonoBehaviour
{
    //public TaskButtonsScript buttonClickedScript;

    private void OnEnable()
    {
        this.transform.parent.parent.GetComponent<GetTasks>().SelectTask(this.transform.parent.GetComponent<TaskObject>());
    }

    private void OnDisable()
    {
        this.transform.parent.parent.GetComponent<GetTasks>().DeselectTask(this.transform.parent.GetComponent<TaskObject>());
        //buttonClickedScript.selectedList.Remove(this.transform.parent.GetComponent<TaskObject>());
    }
}
