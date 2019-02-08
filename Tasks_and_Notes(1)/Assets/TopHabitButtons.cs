using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TopHabitButtons : MonoBehaviour
{
    public Button backB;
    public Button deleteB;
    public HabitButtonsScript bottomBScript;
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
        foreach (HabitObject habit in bottomBScript.selectedList)
        {
            deleteList.Add(habit.transform.Find("HabitButton").Find("HabitClickedPanel").gameObject);
        }
        foreach (GameObject habit in deleteList)
        {
            //Destroy(habit);
            habit.SetActive(false);
        }
        bottomBScript.selectedList = new List<HabitObject>();
    }

    private void DeleteB()
    {
        //TODO: punishments? deduct points?
        //this.transform.parent.gameObject.SetActive(false);
        foreach (HabitObject habit in bottomBScript.selectedList)
        {
            AppControl.control.habitsTrashList.Add(habit.myHabit);
            AppControl.control.habitsList.Remove(habit.myHabit);
            AppControl.control.snapsList.Remove(habit.myHabit);
        }

        bottomBScript.selectedList = new List<HabitObject>();
        allUI.SetActive(false);
        allUI.SetActive(true);


    }
}