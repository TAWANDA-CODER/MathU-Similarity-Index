//Imports
import 'package:client/equationOverview.dart';
import 'package:flutter/material.dart';
import 'package:client/apiInterface.dart';

/*
NOTE
################################################################################
This serves as a template for each saved item
################################################################################
*/

//Code
class SavedResultItem extends StatefulWidget {
  const SavedResultItem(
      {Key? key, required this.equation, required this.problemID})
      : super(key: key);

  final String equation, problemID;

  @override
  State<SavedResultItem> createState() => _SavedResultItemState();
}

class _SavedResultItemState extends State<SavedResultItem> {
  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.fromLTRB(50.0, 10.0, 50.0, 0),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(10.0, 10.0, 10.0, 10.0),
        child: ListTile(
          //onTap: goToEquation,
          title: Text(
            widget.equation,
            style: TextStyle(
              letterSpacing: 2.0,
              wordSpacing: 4.5,
              fontSize: 24.0,
            ),
          ),
          leading: (apiObj.getIsLoggedIn())
              ? IconButton(
                  onPressed: removeFromFavorites,
                  icon: Icon(Icons.delete_outline),
                )
              : null,
          trailing: Icon(Icons.arrow_forward_ios),
        ),
      ),
    );
  }

  void removeFromFavorites() async {
    /*
    @TODO
    1. Make an API_Interface Object
    2. Use apiObj to delete item from saved table
    */

    String uid = apiObj.getLocalUserID();
    bool successful = await apiObj.removeSavedResult(uid, widget.problemID);

    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: (successful)
          ? Text('Yay! Success!')
          : Text('Woops, Something went wrong...'),
      width: 400,
      behavior: SnackBarBehavior.floating,
      duration: const Duration(milliseconds: 1500),
      padding: EdgeInsets.all(10),
    ));
  }

  /* void goToEquation() {
    Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) => EquationOverview(
                equation: widget.equation,
                conf_score: widget.conf_score,
                problemID: widget.problemID)));
  } */
}
