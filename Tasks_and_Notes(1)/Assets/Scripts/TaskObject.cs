using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

public class TaskObject : MonoBehaviour {
    public string taskName;
    public string taskFolder;
    public DateTime dueDate;
    public bool optional;
    public int repeatType;  // 0 = none, 1 = daily, 2 = weekly, 3 = monthly, 4 = yearly
    public int priority;
    public List<string> userTags;
    public List<CommentObject> comments;
    public TaskObject myParentTask;
    public Text nameLabel;
    public Text dateLabel;
    public TaskObject myTask;
    public RectTransform clickedPanel;

    void Start ()
    {
        nameLabel.text = taskName;
        if (dueDate != Convert.ToDateTime("1/1/0001"))
        {
            if (dueDate.TimeOfDay != new TimeSpan(0, 0, 0))
            {
                if (dueDate.Subtract(DateTime.Now).Days < 7 && dueDate.Subtract(DateTime.Now).Days >=0)
                {
                    dateLabel.text = Convert.ToString(dueDate.DayOfWeek)+" "+ Convert.ToString(dueDate.ToShortTimeString());
                }
                else
                {
                    dateLabel.text = Convert.ToString(dueDate.ToShortDateString()) + " " + Convert.ToString(dueDate.ToShortTimeString());
                }
            }
            else
            {
                if (dueDate.Subtract(DateTime.Now).Days < 7 && dueDate.Subtract(DateTime.Now).Days >= 0)
                {
                    dateLabel.text = Convert.ToString(dueDate.DayOfWeek);
                }
                else
                {
                    dateLabel.text = Convert.ToString(dueDate.ToShortDateString());
                }
            }
        }
        else
        {
            dateLabel.text = "";
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
            this.GetComponent<LayoutElement>().minHeight = height +30;

            clickedPanel.sizeDelta = new Vector2(trans.sizeDelta.x, height + 30);


            trans.sizeDelta = new Vector2(trans.sizeDelta.x, height + 30);
            //dateLabel.transform.position = new Vector2(dateLabel.transform.position.x, 0);
        }

    }
}