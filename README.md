<h1>Decision Tree Classifier</h1>
<h4>Machine Learning</h4>

This is a project that implements ID3 algorithm for decision tree classifier.

Decision tree learning uses a decision tree as a predictive model which maps observations about an item (represented in the branches) to conclusions about the item's target value (represented in the leaves).

It is one of the predictive modelling approaches used in statistics, data mining and machine learning. Tree models where the target variable can take a finite set of values are called classification trees; in these tree structures, leaves represent class labels and branches represent conjunctions of features that lead to those class labels.

<h2>Algorith reference</h2>

<ul>
  <li>
    Refer to <a href ="http://romisatriawahono.net/lecture/dm/book/Han%20-%20Data%20Mining%20Concepts%20and%20Techniques%203rd%20Edition%20-%202012.pdf">
    Section 8.2 <a> for complete algorithm (Data Mining : Concepts and Techniques : Concepts and Techniques (3rd Edition) by Jaiwei Han , )
  </li>
  <li>
    Here is a link to a useful <a href="http://www-users.cs.umn.edu/~kumar/dmbook/dmslides/chap4_basic_classification.pdf">resource</a>
  </li>
</ul>

<h2> Motivation</h2>

<ul>
  <li>
    Most of the classifiers including the one in sklearn take only numerical attributes as input. They 
    <strong>convert categorical attributes into numerical values</strong> and apply corresponding numerical classification algorithms.
  </li>
  <li> 
    In most of the decision tree classifiers if categorical attributes are available they convert it into numerical attributes and 
    <strong>distort the original decision tree</strong>.
  </li>
  <li>
    They normally don't provide us the flexibility to select our own root attribute. ( Sometimes by external evaluation or intuition we can fix the root attribute )
  </li>
</ul>

<h2>Advantages</h2>
<ul>
  <li>
    The decision tree classifier we implemented is based on ID3 algorithm. It take both numerical, categorical, and boolean attributes
  </li>
  <li>
    It don't distort the decision tree.
  </li>
  <li>
    It provides flexibility to fix our own root attribute.
  </li>
  <li>
    We can predetermine the tree max-height.
  </li>
</ul>

<h2>Major Dependencies</h2>
<ul>
  <li>Python 2.7</li>
  <li>Pandas</li>
  <li>sklearn</li>
  <li>numpy</li>
</ul>
