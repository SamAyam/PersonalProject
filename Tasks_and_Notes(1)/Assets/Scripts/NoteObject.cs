using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

//[Serializable]
public class NoteObject : MonoBehaviour
{
    public string noteName;
    public string notebook;
    public string noteString;
    public DateTime createdDate;
    public DateTime modifiedDate;
    public Text nameLabel;
    public Button button;
    //public SelectedNotesScript selected;


    public NoteObject myNote;
    public RectTransform clickedPanel;

    void Start()
    {
        nameLabel.text = noteName; // + "        -------- " + Convert.ToString(createdDate.ToShortDateString()) + " " + Convert.ToString(createdDate.ToShortTimeString());
        //button.onClick.AddListener(delegate { EditB(); });
        Resize();
    }

    public void Resize()
    {
        TextGenerator textGen = new TextGenerator();
        TextGenerationSettings generationSettings = nameLabel.GetGenerationSettings(nameLabel.rectTransform.rect.size);
        float height = textGen.GetPreferredHeight(nameLabel.text, generationSettings);


        RectTransform trans = GetComponent<RectTransform>();
        if (height >= trans.sizeDelta.y)
        {
            this.GetComponent<LayoutElement>().minHeight = height;
            nameLabel.GetComponent<RectTransform>().sizeDelta = new Vector2(nameLabel.GetComponent<RectTransform>().sizeDelta.x, height);
            clickedPanel.sizeDelta = new Vector2(trans.sizeDelta.x, height);
        }
    }


    //private void EditB()
    //{
    //        editSnapWindow.habitToEdit = this.transform.parent.GetComponent<HabitObject>().myHabit;
    //        editSnapWindow.gameObject.SetActive(true);
    //        saveSnapButton.gameObject.SetActive(true);

    //        editSnapWindow.PrepScreen();



    //}
}
