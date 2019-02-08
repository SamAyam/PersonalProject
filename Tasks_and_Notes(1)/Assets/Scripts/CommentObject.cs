using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

[Serializable]
public class CommentObject : MonoBehaviour
{
    public string commentString;
    public DateTime createdDate;
    public Text nameLabel;
    public Text dateLabel;
    public CommentObject myComment;
    public TaskObject myTask;
    public RectTransform clickedPanel;

    void Start()
    {
        nameLabel.text = commentString;
        dateLabel.text = Convert.ToString(createdDate.ToShortDateString()) + " " + Convert.ToString(createdDate.ToShortTimeString());
        Resize();
    }

    public void Resize()
    { 
        TextGenerator textGen = new TextGenerator();
        TextGenerationSettings generationSettings = nameLabel.GetGenerationSettings(nameLabel.rectTransform.rect.size);
        float height = textGen.GetPreferredHeight(nameLabel.text, generationSettings);


        RectTransform trans = GetComponent<RectTransform>();
        if (height >= trans.sizeDelta.x)
        {
            this.GetComponent<LayoutElement>().minHeight = height + 30;

            clickedPanel.sizeDelta = new Vector2(trans.sizeDelta.x, height + 30);


            trans.sizeDelta = new Vector2(trans.sizeDelta.x, height + 30);
            //dateLabel.transform.position = new Vector2(dateLabel.transform.position.x, 0);

            clickedPanel.sizeDelta = new Vector2(trans.sizeDelta.x, height);
        }
    }
}
