using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveTop : MonoBehaviour {
    public GameObject thisButton;
    public GameObject top;
    public Transform moveHere;
    public GameObject winButton;

    public void MoveDown()
    {
        top.transform.position = moveHere.position;
        winButton.SetActive(true);
        thisButton.SetActive(false);
    }
}
