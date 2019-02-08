using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class NavigationDrawerScript : MonoBehaviour {
    public Dropdown panelSelect;  // Values: 0 = Tasks, 1 = Habits, 2 = Projects, 3 = Goals, 4 = notes
    public GameObject taskPanel;
    public GameObject habitPanel;
    public GameObject projectPanel;
    public GameObject goalPanel;
    public GameObject notePanel;

    private void OnEnable()
    {
        SetPanel();
    }

    public void SetPanel()
    {
        if (panelSelect.value == 0)  // 0 = Tasks
        {
            taskPanel.SetActive(true);
            habitPanel.SetActive(false);
            projectPanel.SetActive(false);
            goalPanel.SetActive(false);
            notePanel.SetActive(false);
        }
        else if (panelSelect.value == 1)  // 1 = Habits
        {
            taskPanel.SetActive(false);
            habitPanel.SetActive(true);
            projectPanel.SetActive(false);
            goalPanel.SetActive(false);
            notePanel.SetActive(false);
        }
        else if (panelSelect.value == 2)  // 2 = Projects
        {
            taskPanel.SetActive(false);
            habitPanel.SetActive(false);
            projectPanel.SetActive(true);
            goalPanel.SetActive(false);
            notePanel.SetActive(false);
        }
        else if (panelSelect.value == 3)  // 3 = Goals
        {
            taskPanel.SetActive(false);
            habitPanel.SetActive(false);
            projectPanel.SetActive(false);
            goalPanel.SetActive(true);
            notePanel.SetActive(false);
        }
        else if (panelSelect.value == 4)  // 4 = Notes
        {
            taskPanel.SetActive(false);
            habitPanel.SetActive(false);
            projectPanel.SetActive(false);
            goalPanel.SetActive(false);
            notePanel.SetActive(true);
        }
    }
}
