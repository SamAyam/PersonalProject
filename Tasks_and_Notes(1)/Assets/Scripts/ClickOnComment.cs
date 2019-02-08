using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ClickOnComment : MonoBehaviour {
    public AddCommentToTask addComment;


    private void OnEnable()
    {
        addComment.selectedComments.Add(transform.parent.GetComponent<CommentObject>());
    }

    private void OnDisable()
    {
        addComment.selectedComments.Remove(transform.parent.GetComponent<CommentObject>());
    }
}
