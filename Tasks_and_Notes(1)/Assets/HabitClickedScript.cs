using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HabitClickedScript : MonoBehaviour
{
    private void OnEnable()
    {
        this.transform.parent.parent.parent.GetComponent<GetHabits>().SelectHabit(this.transform.parent.parent.GetComponent<HabitObject>());
    }

    private void OnDisable()
    {
        this.transform.parent.parent.parent.GetComponent<GetHabits>().DeselectHabit(this.transform.parent.parent.GetComponent<HabitObject>());
    }
}
