using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEngine.UI;

[Serializable]
public class DoItObject : MonoBehaviour {
    public string doItName = "";  // newtask, anotherhabit, etc
    public string howToDoIt = "";
    public Text nameLabel;

    // Use this for initialization
    void Start ()
    {
        nameLabel.text = doItName;
    }
}
