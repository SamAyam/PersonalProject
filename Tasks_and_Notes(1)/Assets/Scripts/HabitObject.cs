using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEngine.UI;

public class HabitObject : MonoBehaviour {
    public string habitName;
    public int repeatType;     // This can be 4 = "yearly", 3 = "monthly", 2 = "weekly", 1 = "daily", 0 = "" (constant)
    public List<DoItObject> doItList;
    public int rewardPoints;
    public int missedPoints;
    //public object rewardToken;
    //public object missedLoss;
    public bool showPoints;
    public HabitObject myHabit;
    public bool asleep = false;
    public bool done = false;
    public DateTime resetDate;
    public RectTransform clickedPanel;

    public Text nameLabel;

    public int inARow = 0;
    public bool missed = false;
    public GameObject redCircle;
    public GameObject yellowCircle;
    public GameObject blueCircle;

    public Text dayStreak;

    public List<DayOfWeek> daysOfWeek = new List<DayOfWeek>();

    // Use this for initialization
    public void Start ()
    {
        nameLabel.text = habitName;
        dayStreak.text = Convert.ToString(inARow);
        if (inARow == 0)
        {
            yellowCircle.SetActive(true);
            redCircle.SetActive(false);
            blueCircle.SetActive(false);
        }
        else
        {
            if (missed)
            {
                yellowCircle.SetActive(false);
                redCircle.SetActive(true);
                blueCircle.SetActive(false);
            }
            else
            {
                yellowCircle.SetActive(false);
                redCircle.SetActive(false);
                blueCircle.SetActive(true);
            }
        }
        Resize();
    }

    public void Resize()
    {
        TextGenerator textGen = new TextGenerator();
        TextGenerationSettings generationSettings = nameLabel.GetGenerationSettings(nameLabel.rectTransform.rect.size);
        float height = textGen.GetPreferredHeight(nameLabel.text, generationSettings);

        RectTransform trans = GetComponentInChildren<RectTransform>();
        if (height >= trans.sizeDelta.y)
        {
            this.GetComponent<LayoutElement>().minHeight = height;

            clickedPanel.sizeDelta = new Vector2(trans.sizeDelta.x, height);


            trans.sizeDelta = new Vector2(trans.sizeDelta.x, height);
        }

    }

}
