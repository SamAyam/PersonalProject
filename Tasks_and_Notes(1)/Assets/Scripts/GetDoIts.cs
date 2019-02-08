using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetDoIts : MonoBehaviour
{
    public DoItObject blankDoIt;
    public NewHabitScript parentHabitPanel;


    public void DrawTasks()
    {
        if (AppControl.control != null)
        {
            Clear();
            for (int i = 0; i < parentHabitPanel.doItList.Count; i++)
            {
                DoItObject newDoItInstance = Instantiate(blankDoIt) as DoItObject;
                newDoItInstance.doItName = parentHabitPanel.doItList[i].doItName;
                newDoItInstance.howToDoIt = parentHabitPanel.doItList[i].howToDoIt;
                newDoItInstance.transform.SetParent(this.transform);
                newDoItInstance.GetComponent<RectTransform>().localScale = Vector3.one;

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
