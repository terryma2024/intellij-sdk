
# CODE_OF_CONDUCT.md
## Code of Conduct

This project and the corresponding community is governed by the [JetBrains Open Source and Community Code of Conduct](https://github.com/jetbrains#code-of-conduct).
Please make sure you read it.


# kotlin_demo/README.md
# Kotlin Demo [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]

> Plugin Sample has been removed.
> Refer to
> [Kotlin for Plugin Developers in IntelliJ SDK Docs][docs:kotlin]
> on how to set up Kotlin for your plugin project.

[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:actions]: https://plugins.jetbrains.com/docs/intellij/basic-action-system.html
[docs:kotlin]: https://plugins.jetbrains.com/docs/intellij/kotlin.html


# settings/README.md
# Settings Example [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Settings Tutorial in IntelliJ SDK Docs][docs:settings_tutorial]*

## Quickstart

This project illustrates a custom Application-level Settings through the implementation of:
- `AppSettingsConfigurable` is analogous to a Controller in the MVC model – it interacts with the other two Settings classes and the IntelliJ Platform,
- `AppSettings` is like a Model because it stores the Settings persistently,
- `AppSettingsComponent` is similar to a View because it displays and captures edits to the values of the Settings.

### Extension Points

| Name                                   | Implementation                                          | Extension Point Class      |
|----------------------------------------|---------------------------------------------------------|----------------------------|
| `com.intellij.applicationConfigurable` | [AppSettingsConfigurable][file:AppSettingsConfigurable] | `Configurable`             |
| `com.intellij.applicationService`      | [AppSettings][file:AppSettings]                         | `PersistentStateComponent` |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:settings_tutorial]: https://plugins.jetbrains.com/docs/intellij/settings-tutorial.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:AppSettingsConfigurable]: ./src/main/java/org/intellij/sdk/settings/AppSettingsConfigurable.java
[file:AppSettings]: ./src/main/java/org/intellij/sdk/settings/AppSettings.java


# settings/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# settings/settings.gradle.kts
```kotlin
rootProject.name = "settings"

```

# settings/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# settings/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license. -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.settings</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Settings Example</name>

  <!-- please see https://plugins.jetbrains.com/docs/intellij/plugin-compatibility.html
       on how to target different products -->
  <depends>com.intellij.modules.platform</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates implementing a custom settings panel.<br>Adds a settings panel to the <b>Settings</b>
      panel under <b>Tools</b>.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>1.0</b> Initial SDK settings content release for 2020.1</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <applicationConfigurable parentId="tools" instance="org.intellij.sdk.settings.AppSettingsConfigurable"
                             id="org.intellij.sdk.settings.AppSettingsConfigurable"
                             displayName="SDK: Application Settings Example"/>
    <applicationService serviceImplementation="org.intellij.sdk.settings.AppSettings"/>
  </extensions>

</idea-plugin>

```

# settings/src/main/java/org/intellij/sdk/settings/AppSettingsComponent.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.settings;

import com.intellij.ui.components.JBCheckBox;
import com.intellij.ui.components.JBLabel;
import com.intellij.ui.components.JBTextField;
import com.intellij.util.ui.FormBuilder;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

/**
 * Supports creating and managing a {@link JPanel} for the Settings Dialog.
 */
public class AppSettingsComponent {

  private final JPanel myMainPanel;
  private final JBTextField myUserNameText = new JBTextField();
  private final JBCheckBox myIdeaUserStatus = new JBCheckBox("IntelliJ IDEA user");

  public AppSettingsComponent() {
    myMainPanel = FormBuilder.createFormBuilder()
        .addLabeledComponent(new JBLabel("User name:"), myUserNameText, 1, false)
        .addComponent(myIdeaUserStatus, 1)
        .addComponentFillVertically(new JPanel(), 0)
        .getPanel();
  }

  public JPanel getPanel() {
    return myMainPanel;
  }

  public JComponent getPreferredFocusedComponent() {
    return myUserNameText;
  }

  @NotNull
  public String getUserNameText() {
    return myUserNameText.getText();
  }

  public void setUserNameText(@NotNull String newText) {
    myUserNameText.setText(newText);
  }

  public boolean getIdeaUserStatus() {
    return myIdeaUserStatus.isSelected();
  }

  public void setIdeaUserStatus(boolean newStatus) {
    myIdeaUserStatus.setSelected(newStatus);
  }

}

```

# settings/src/main/java/org/intellij/sdk/settings/AppSettings.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.settings;

import com.intellij.openapi.application.ApplicationManager;
import com.intellij.openapi.components.PersistentStateComponent;
import com.intellij.openapi.components.State;
import com.intellij.openapi.components.Storage;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

/*
 * Supports storing the application settings in a persistent way.
 * The {@link com.intellij.openapi.components.State State} and {@link Storage}
 * annotations define the name of the data and the filename where these persistent
 * application settings are stored.
 */

@State(
    name = "org.intellij.sdk.settings.AppSettings",
    storages = @Storage("SdkSettingsPlugin.xml")
)
final class AppSettings
    implements PersistentStateComponent<AppSettings.State> {

  static class State {
    @NonNls
    public String userId = "John Smith";
    public boolean ideaStatus = false;
  }

  private State myState = new State();

  static AppSettings getInstance() {
    return ApplicationManager.getApplication()
        .getService(AppSettings.class);
  }

  @Override
  public State getState() {
    return myState;
  }

  @Override
  public void loadState(@NotNull State state) {
    myState = state;
  }

}

```

# settings/src/main/java/org/intellij/sdk/settings/AppSettingsConfigurable.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.
package org.intellij.sdk.settings;

import com.intellij.openapi.options.Configurable;
import org.jetbrains.annotations.Nls;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.util.Objects;

/**
 * Provides controller functionality for application settings.
 */
final class AppSettingsConfigurable implements Configurable {

  private AppSettingsComponent mySettingsComponent;

  // A default constructor with no arguments is required because
  // this implementation is registered as an applicationConfigurable

  @Nls(capitalization = Nls.Capitalization.Title)
  @Override
  public String getDisplayName() {
    return "SDK: Application Settings Example";
  }

  @Override
  public JComponent getPreferredFocusedComponent() {
    return mySettingsComponent.getPreferredFocusedComponent();
  }

  @Nullable
  @Override
  public JComponent createComponent() {
    mySettingsComponent = new AppSettingsComponent();
    return mySettingsComponent.getPanel();
  }

  @Override
  public boolean isModified() {
    AppSettings.State state =
        Objects.requireNonNull(AppSettings.getInstance().getState());
    return !mySettingsComponent.getUserNameText().equals(state.userId) ||
        mySettingsComponent.getIdeaUserStatus() != state.ideaStatus;
  }

  @Override
  public void apply() {
    AppSettings.State state =
        Objects.requireNonNull(AppSettings.getInstance().getState());
    state.userId = mySettingsComponent.getUserNameText();
    state.ideaStatus = mySettingsComponent.getIdeaUserStatus();
  }

  @Override
  public void reset() {
    AppSettings.State state =
        Objects.requireNonNull(AppSettings.getInstance().getState());
    mySettingsComponent.setUserNameText(state.userId);
    mySettingsComponent.setIdeaUserStatus(state.ideaStatus);
  }

  @Override
  public void disposeUIResources() {
    mySettingsComponent = null;
  }

}

```

# project_model/README.md
# Project Model Sample [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Project in IntelliJ SDK Docs][docs:project], [SDK in IntelliJ SDK Docs][docs:sdk], [Library in IntelliJ SDK Docs][docs:library]*

## Quickstart

Project Model Sample project provides five actions that present data extracted using `ProjectRootManager` instance in the message dialogs.
Within the implemented actions, you will be able to:
- fetch libraries used in the project,
- retrieve the information about the module details,
- rename the used SDK,
- get the content source roots,
- or extend the project dependencies with an additional library.

### Actions

| ID                                | Implementation                                                    | Base Action Class |
|-----------------------------------|-------------------------------------------------------------------|-------------------|
| `ProjectModel.SourceRoots`        | [ShowSourceRootsActions][file:ShowSourceRootsActions]             | `AnAction`        |
| `ProjectModel.ProjectSdk`         | [ProjectSdkAction][file:ProjectSdkAction]                         | `AnAction`        |
| `ProjectModel.ProjectFileIndex`   | [ProjectFileIndexSampleAction][file:ProjectFileIndexSampleAction] | `AnAction`        |
| `ProjectModel.ModificationAction` | [ModificationAction][file:ModificationAction]                     | `AnAction`        |
| `ProjectModel.LibrariesAction`    | [LibrariesAction][file:LibrariesAction]                           | `AnAction`        |

*Reference: [Action System in IntelliJ SDK Docs][docs:actions]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:actions]: https://plugins.jetbrains.com/docs/intellij/basic-action-system.html
[docs:project]: https://plugins.jetbrains.com/docs/intellij/project.html
[docs:sdk]: https://plugins.jetbrains.com/docs/intellij/sdk.html
[docs:library]: https://plugins.jetbrains.com/docs/intellij/library.html

[file:ShowSourceRootsActions]: ./src/main/java/org/intellij/sdk/project/model/ShowSourceRootsActions.java
[file:ProjectSdkAction]: ./src/main/java/org/intellij/sdk/project/model/ProjectSdkAction.java
[file:ProjectFileIndexSampleAction]: ./src/main/java/org/intellij/sdk/project/model/ProjectFileIndexSampleAction.java
[file:ModificationAction]: ./src/main/java/org/intellij/sdk/project/model/ModificationAction.java
[file:LibrariesAction]: ./src/main/java/org/intellij/sdk/project/model/LibrariesAction.java


# project_model/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
  plugins.set(listOf("com.intellij.java"))
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# project_model/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "project_model"

```

# project_model/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# project_model/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.project.model</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Project Model Sample</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.platform</depends>
  <depends>com.intellij.java</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates various aspects of interacting with project model.<br>Adds menu items to
      <b>Tools</b> and <b>Editor Context</b> menus.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin, change plugin ID</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <actions>
    <action id="ProjectModel.SourceRoots" class="org.intellij.sdk.project.model.ShowSourceRootsActions"
            text="Show Source Roots"
            description="Illustrates how to get source roots"
            icon="SdkIcons.Sdk_default_icon">
      <add-to-group group-id="ToolsMenu" anchor="first"/>
    </action>
    <action id="ProjectModel.ProjectSdk" class="org.intellij.sdk.project.model.ProjectSdkAction"
            text="Show Sdk Info"
            description="Illustrates how to get Sdk info"
            icon="SdkIcons.Sdk_default_icon">
      <add-to-group group-id="ToolsMenu" anchor="after" relative-to-action="ProjectModel.SourceRoots"/>
    </action>
    <action id="ProjectModel.ProjectFileIndex"
            class="org.intellij.sdk.project.model.ProjectFileIndexSampleAction"
            text="FileProjectIndex in Action"
            description="Illustrates how to get source roots"
            icon="SdkIcons.Sdk_default_icon">
      <add-to-group group-id="EditorPopupMenu" anchor="last"/>
    </action>
    <action id="ProjectModel.ModificationAction" class="org.intellij.sdk.project.model.ModificationAction"
            text="Project Modification in Action"
            description="Illustrates how to get source roots"
            icon="SdkIcons.Sdk_default_icon">
      <add-to-group group-id="EditorPopupMenu" anchor="last"/>
    </action>
    <action id="ProjectModel.LibrariesAction" class="org.intellij.sdk.project.model.LibrariesAction"
            text="Libraries for File"
            description="Illustrates accessing libraries"
            icon="SdkIcons.Sdk_default_icon">
      <add-to-group group-id="EditorPopupMenu" anchor="last"/>
    </action>
  </actions>

</idea-plugin>

```

# project_model/src/main/java/org/intellij/sdk/project/model/LibrariesAction.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.project.model;

import com.intellij.openapi.actionSystem.ActionUpdateThread;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.roots.*;
import com.intellij.openapi.roots.libraries.Library;
import com.intellij.openapi.ui.Messages;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.pom.Navigatable;
import com.intellij.psi.PsiClass;
import com.intellij.psi.PsiFile;
import org.jetbrains.annotations.NotNull;

public class LibrariesAction extends AnAction {

  @Override
  public @NotNull ActionUpdateThread getActionUpdateThread() {
    return ActionUpdateThread.BGT;
  }

  @Override
  public void update(@NotNull final AnActionEvent event) {
    Project project = event.getProject();
    if (project == null) {
      return;
    }
    Navigatable element = event.getData(CommonDataKeys.NAVIGATABLE);
    if (element instanceof PsiClass) {
      PsiFile psiFile = ((PsiClass) element).getContainingFile();
      if (psiFile == null) {
        return;
      }
      VirtualFile virtualFile = psiFile.getVirtualFile();
      if (virtualFile == null) {
        return;
      }
      event.getPresentation().setEnabledAndVisible(true);
    }
  }

  @Override
  public void actionPerformed(@NotNull AnActionEvent event) {
    Project project = event.getProject();
    if (project == null) {
      return;
    }
    Navigatable element = event.getData(CommonDataKeys.NAVIGATABLE);
    if (element instanceof PsiClass) {
      PsiFile psiFile = ((PsiClass) element).getContainingFile();
      if (psiFile == null) {
        return;
      }
      VirtualFile virtualFile = psiFile.getVirtualFile();
      if (virtualFile == null) {
        return;
      }
      final ProjectFileIndex fileIndex = ProjectRootManager.getInstance(project).getFileIndex();
      StringBuilder jars = new StringBuilder();
      for (OrderEntry orderEntry : fileIndex.getOrderEntriesForFile(virtualFile)) {
        if (orderEntry instanceof LibraryOrderEntry libraryEntry) {
          final Library library = libraryEntry.getLibrary();
          if (library == null) {
            continue;
          }
          VirtualFile[] files = library.getFiles(OrderRootType.CLASSES);
          if (files.length == 0) {
            continue;
          }
          for (VirtualFile jar : files) {
            jars.append(jar.getName()).append(", ");
          }
        }
      }
      String fileAndLibs;
      if (jars.length() > 0) {
        fileAndLibs = virtualFile.getName() + ": " + jars;
      } else {
        fileAndLibs = "None";
      }
      Messages.showInfoMessage("Libraries for file: " + fileAndLibs,
          "Libraries Info");
    }
  }

}

```

# project_model/src/main/java/org/intellij/sdk/project/model/ProjectFileIndexSampleAction.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.project.model;

import com.intellij.openapi.actionSystem.ActionUpdateThread;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.editor.Document;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.fileEditor.FileDocumentManager;
import com.intellij.openapi.module.Module;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.roots.ProjectFileIndex;
import com.intellij.openapi.roots.ProjectRootManager;
import com.intellij.openapi.ui.Messages;
import com.intellij.openapi.vfs.VirtualFile;
import org.jetbrains.annotations.NotNull;

public class ProjectFileIndexSampleAction extends AnAction {

  @Override
  public @NotNull ActionUpdateThread getActionUpdateThread() {
    return ActionUpdateThread.BGT;
  }

  @Override
  public void update(@NotNull final AnActionEvent event) {
    Project project = event.getProject();
    final Editor editor = event.getData(CommonDataKeys.EDITOR);
    boolean visibility = project != null && editor != null;
    event.getPresentation().setEnabledAndVisible(visibility);
  }

  @Override
  public void actionPerformed(@NotNull final AnActionEvent event) {
    Project project = event.getProject();
    final Editor editor = event.getData(CommonDataKeys.EDITOR);
    if (project == null || editor == null) {
      return;
    }

    Document document = editor.getDocument();
    FileDocumentManager fileDocumentManager = FileDocumentManager.getInstance();
    VirtualFile virtualFile = fileDocumentManager.getFile(document);
    ProjectFileIndex projectFileIndex = ProjectRootManager.getInstance(project).getFileIndex();
    if (virtualFile != null) {
      Module module = projectFileIndex.getModuleForFile(virtualFile);
      String moduleName;
      moduleName = module != null ? module.getName() : "No module defined for file";

      VirtualFile moduleContentRoot = projectFileIndex.getContentRootForFile(virtualFile);
      boolean isLibraryFile = projectFileIndex.isInLibrary(virtualFile);
      boolean isInLibraryClasses = projectFileIndex.isInLibraryClasses(virtualFile);
      boolean isInLibrarySource = projectFileIndex.isInLibrarySource(virtualFile);
      Messages.showInfoMessage("Module: " + moduleName + "\n" +
              "Module content root: " + moduleContentRoot + "\n" +
              "Is library file: " + isLibraryFile + "\n" +
              "Is in library classes: " + isInLibraryClasses +
              ", Is in library source: " + isInLibrarySource,
          "Main File Info for" + virtualFile.getName());
    }
  }

}

```

# project_model/src/main/java/org/intellij/sdk/project/model/ProjectSdkAction.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.project.model;

import com.intellij.openapi.actionSystem.ActionUpdateThread;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.projectRoots.Sdk;
import com.intellij.openapi.roots.ProjectRootManager;
import com.intellij.openapi.ui.Messages;
import org.jetbrains.annotations.NotNull;

public class ProjectSdkAction extends AnAction {

  @Override
  public @NotNull ActionUpdateThread getActionUpdateThread() {
    return ActionUpdateThread.BGT;
  }

  @Override
  public void actionPerformed(@NotNull final AnActionEvent event) {
    Project project = event.getProject();
    if (project != null) {
      Sdk sdk = ProjectRootManager.getInstance(project).getProjectSdk();
      if (sdk != null) {
        String projectSDKName = sdk.getName();
        String newProjectSdkName = "New Sdk Name";
        ProjectRootManager.getInstance(project).setProjectSdkName(newProjectSdkName, sdk.getSdkType().getName());
        Messages.showInfoMessage(projectSDKName + " has changed to " + newProjectSdkName, "Project Sdk Info");
      }
    }
  }

  @Override
  public void update(@NotNull final AnActionEvent event) {
    Project project = event.getProject();
    if (project != null) {
      Sdk sdk = ProjectRootManager.getInstance(project).getProjectSdk();
      event.getPresentation().setEnabledAndVisible(sdk != null);
    }
  }

}

```

# project_model/src/main/java/org/intellij/sdk/project/model/ModificationAction.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.project.model;

import com.intellij.openapi.actionSystem.ActionUpdateThread;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.module.Module;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.roots.ModuleRootManager;
import com.intellij.openapi.roots.ModuleRootModificationUtil;
import com.intellij.openapi.roots.ProjectFileIndex;
import com.intellij.openapi.roots.ProjectRootManager;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.pom.Navigatable;
import com.intellij.psi.PsiClass;
import com.intellij.psi.PsiFile;
import org.jetbrains.annotations.NotNull;

public class ModificationAction extends AnAction {

  @Override
  public @NotNull ActionUpdateThread getActionUpdateThread() {
    return ActionUpdateThread.BGT;
  }

  @Override
  public void actionPerformed(@NotNull final AnActionEvent event) {
    Project project = event.getProject();
    if (project == null) {
      return;
    }
    Navigatable element = event.getData(CommonDataKeys.NAVIGATABLE);
    if (element instanceof PsiClass) {
      PsiFile file = ((PsiClass) element).getContainingFile();
      if (file == null) {
        return;
      }
      final VirtualFile virtualFile = file.getVirtualFile();
      if (virtualFile == null) {
        return;
      }
      final ProjectFileIndex fileIndex = ProjectRootManager.getInstance(project).getFileIndex();
      final Module module = fileIndex.getModuleForFile(virtualFile);
      if (module == null) {
        return;
      }
      if (!ModuleRootManager.getInstance(module).getFileIndex().isInContent(virtualFile)) {
        ModuleRootModificationUtil.addModuleLibrary(module, virtualFile.getUrl());
      }
    }

  }

  @Override
  public void update(@NotNull final AnActionEvent event) {
    Project project = event.getProject();
    Navigatable element = event.getData(CommonDataKeys.NAVIGATABLE);
    event.getPresentation().setEnabledAndVisible(project != null && element != null);
  }

}

```

# project_model/src/main/java/org/intellij/sdk/project/model/ShowSourceRootsActions.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.project.model;

import com.intellij.openapi.actionSystem.ActionUpdateThread;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.roots.ProjectRootManager;
import com.intellij.openapi.ui.Messages;
import com.intellij.openapi.vfs.VirtualFile;
import org.jetbrains.annotations.NotNull;

public class ShowSourceRootsActions extends AnAction {

  @Override
  public @NotNull ActionUpdateThread getActionUpdateThread() {
    return ActionUpdateThread.BGT;
  }

  @Override
  public void actionPerformed(@NotNull final AnActionEvent event) {
    Project project = event.getProject();
    if (project == null) {
      return;
    }

    String projectName = project.getName();
    StringBuilder sourceRootsList = new StringBuilder();
    VirtualFile[] vFiles = ProjectRootManager.getInstance(project).getContentSourceRoots();
    for (VirtualFile file : vFiles) {
      sourceRootsList.append(file.getUrl()).append("\n");
    }
    Messages.showInfoMessage(
        "Source roots for the " + projectName + " plugin:\n" + sourceRootsList,
        "Project Properties"
    );
  }

  @Override
  public void update(@NotNull final AnActionEvent event) {
    boolean visibility = event.getProject() != null;
    event.getPresentation().setEnabled(visibility);
    event.getPresentation().setVisible(visibility);
  }

}

```

# project_model/src/main/java/icons/SdkIcons.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package icons;

import com.intellij.openapi.util.IconLoader;

import javax.swing.*;

public class SdkIcons {

  public static final Icon Sdk_default_icon = IconLoader.getIcon("/icons/sdk_16.svg", SdkIcons.class);

}

```

# max_opened_projects/README.md
# Maximum Open Projects Sample [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Plugin Services in IntelliJ SDK Docs][docs:plugin_services]*

## Quickstart

Maximum Open Projects Sample implements a `StartupActivity` extension point to run on project open as well as a
`ProjectManagerListener` for tracking projects being closed.
Both use `ProjectCountingService` application-level [light service][docs:plugin_services:light_services].
It provides methods to increase and decrease the counter of currently opened projects in the IDE.
When opening more projects than the maximum allowed (3), a message dialog is shown.

### Extension Points

| Name                               | Implementation                                                | Extension Point Class |
|------------------------------------|---------------------------------------------------------------|-----------------------|
| `com.intellij.postStartupActivity` | [ProjectOpenStartupActivity][file:ProjectOpenStartupActivity] | `StartupActivity`     |

### Application Listeners

| Name     | Implementation                                        | Listener Class           |
|----------|-------------------------------------------------------|--------------------------|
| listener | [ProjectOpenCloseListener][file:ProjectCloseListener] | `ProjectManagerListener` |

*Reference: [Plugin Listeners in IntelliJ SDK Docs][docs:listeners]*

[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:plugin_services]: https://plugins.jetbrains.com/docs/intellij/plugin-services.html
[docs:plugin_services:light_services]: https://plugins.jetbrains.com/docs/intellij/plugin-services.html#light-services
[docs:listeners]: https://plugins.jetbrains.com/docs/intellij/plugin-listeners.html

[file:ProjectOpenStartupActivity]: ./src/main/kotlin/org/intellij/sdk/maxOpenProjects/ProjectOpenStartupActivity.kt
[file:ProjectCountingService]: ./src/main/java/org/intellij/sdk/maxOpenProjects/ProjectCountingService.java
[file:ProjectCloseListener]: ./src/main/java/org/intellij/sdk/maxOpenProjects/ProjectCloseListener.java


# max_opened_projects/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
  id("org.jetbrains.kotlin.jvm") version "1.9.25"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# max_opened_projects/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "max_opened_projects"

```

# max_opened_projects/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# max_opened_projects/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.maxOpenProjects</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Maximum Open Projects Sample</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.platform</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates adding application services and listeners. Shows warning dialog when more than 3 open projects
      is exceeded.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li>
          <b>2.1.0</b> Remove project component and use listener instead. No longer denies opening additional
          projects. Just notifies the user.
        </li>
        <li><b>2.0.0</b> Convert to Gradle-based plugin.</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <applicationListeners>
    <listener class="org.intellij.sdk.maxOpenProjects.ProjectCloseListener"
              topic="com.intellij.openapi.project.ProjectManagerListener"/>
  </applicationListeners>

  <extensions defaultExtensionNs="com.intellij">
    <postStartupActivity implementation="org.intellij.sdk.maxOpenProjects.ProjectOpenStartupActivity"/>
  </extensions>
</idea-plugin>

```

# max_opened_projects/src/main/java/org/intellij/sdk/maxOpenProjects/ProjectCountingService.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.maxOpenProjects;

import com.intellij.openapi.components.Service;

/**
 * Application service implementation to keep a running count of how many projects are open at a given time.
 */
@Service
public final class ProjectCountingService {

  private final static int MAX_OPEN_PROJECTS_LIMIT = 3;

  private int myOpenProjectCount = 0;

  public void increaseOpenProjectCount() {
    myOpenProjectCount++;
  }

  public void decreaseOpenProjectCount() {
    if (myOpenProjectCount > 0) {
      myOpenProjectCount--;
    }
  }

  public boolean isOpenProjectsLimitExceeded() {
    return myOpenProjectCount > MAX_OPEN_PROJECTS_LIMIT;
  }

}

```

# max_opened_projects/src/main/java/org/intellij/sdk/maxOpenProjects/ProjectCloseListener.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.maxOpenProjects;

import com.intellij.openapi.application.ApplicationManager;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.project.ProjectManagerListener;
import org.jetbrains.annotations.NotNull;

/**
 * Listener to detect project closing.
 */
final class ProjectCloseListener implements ProjectManagerListener {

  @Override
  public void projectClosed(@NotNull Project project) {
    // Get the counting service
    ProjectCountingService projectCountingService =
        ApplicationManager.getApplication().getService(ProjectCountingService.class);
    // Decrement the count because a project just closed
    projectCountingService.decreaseOpenProjectCount();
  }

}

```

# run_configuration/README.md
# Run Configuration Demo [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Run Configurations in IntelliJ SDK Docs][docs:run_configurations]*

## Quickstart

Run Configuration example project provides an implementation of the `com.intellij.configurationType` extension point responsible for adding new options for the Run/Debug Configurations.
In this example, a new *Demo* configuration is added together with `ConfigurationFactory` instance that collects run/debug properties - `scriptName` in this case.

### Extension Points

| Name                             | Implementation                                            | Extension Point Class |
|----------------------------------|-----------------------------------------------------------|-----------------------|
| `com.intellij.configurationType` | [DemoRunConfigurationType][file:DemoRunConfigurationType] | `ConfigurationType`   |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:run_configurations]: https://plugins.jetbrains.com/docs/intellij/run-configurations.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:DemoRunConfigurationType]: ./src/main/java/org/jetbrains/sdk/runConfiguration/DemoRunConfigurationType.java


# run_configuration/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# run_configuration/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "run_configuration"

```

# run_configuration/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# run_configuration/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.runConfiguration</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Run Configuration Demo</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.platform</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Illustration of working with run configurations
      <br>
      See the
      <a href="https://plugins.jetbrains.com/docs/intellij/run-configurations.html">Run Configurations</a>
      for more information.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin.</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <configurationType implementation="org.jetbrains.sdk.runConfiguration.DemoRunConfigurationType"/>
  </extensions>

</idea-plugin>

```

# run_configuration/src/main/java/org/jetbrains/sdk/runConfiguration/DemoRunConfigurationType.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.
package org.jetbrains.sdk.runConfiguration;

import com.intellij.execution.configurations.ConfigurationTypeBase;
import com.intellij.icons.AllIcons;
import com.intellij.openapi.util.NotNullLazyValue;

final class DemoRunConfigurationType extends ConfigurationTypeBase {

  static final String ID = "DemoRunConfiguration";

  DemoRunConfigurationType() {
    super(ID, "Demo", "Demo run configuration type",
        NotNullLazyValue.createValue(() -> AllIcons.Nodes.Console));
    addFactory(new DemoConfigurationFactory(this));
  }

}

```

# run_configuration/src/main/java/org/jetbrains/sdk/runConfiguration/DemoConfigurationFactory.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.jetbrains.sdk.runConfiguration;

import com.intellij.execution.configurations.ConfigurationFactory;
import com.intellij.execution.configurations.ConfigurationType;
import com.intellij.execution.configurations.RunConfiguration;
import com.intellij.openapi.components.BaseState;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class DemoConfigurationFactory extends ConfigurationFactory {

  protected DemoConfigurationFactory(ConfigurationType type) {
    super(type);
  }

  @Override
  public @NotNull String getId() {
    return DemoRunConfigurationType.ID;
  }

  @NotNull
  @Override
  public RunConfiguration createTemplateConfiguration(
      @NotNull Project project) {
    return new DemoRunConfiguration(project, this, "Demo");
  }

  @Nullable
  @Override
  public Class<? extends BaseState> getOptionsClass() {
    return DemoRunConfigurationOptions.class;
  }

}

```

# run_configuration/src/main/java/org/jetbrains/sdk/runConfiguration/DemoRunConfiguration.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.
package org.jetbrains.sdk.runConfiguration;

import com.intellij.execution.ExecutionException;
import com.intellij.execution.Executor;
import com.intellij.execution.configurations.*;
import com.intellij.execution.process.OSProcessHandler;
import com.intellij.execution.process.ProcessHandler;
import com.intellij.execution.process.ProcessHandlerFactory;
import com.intellij.execution.process.ProcessTerminatedListener;
import com.intellij.execution.runners.ExecutionEnvironment;
import com.intellij.openapi.options.SettingsEditor;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class DemoRunConfiguration extends RunConfigurationBase<DemoRunConfigurationOptions> {

  protected DemoRunConfiguration(Project project,
                                 ConfigurationFactory factory,
                                 String name) {
    super(project, factory, name);
  }

  @NotNull
  @Override
  protected DemoRunConfigurationOptions getOptions() {
    return (DemoRunConfigurationOptions) super.getOptions();
  }

  public String getScriptName() {
    return getOptions().getScriptName();
  }

  public void setScriptName(String scriptName) {
    getOptions().setScriptName(scriptName);
  }

  @NotNull
  @Override
  public SettingsEditor<? extends RunConfiguration> getConfigurationEditor() {
    return new DemoSettingsEditor();
  }

  @Nullable
  @Override
  public RunProfileState getState(@NotNull Executor executor,
                                  @NotNull ExecutionEnvironment environment) {
    return new CommandLineState(environment) {
      @NotNull
      @Override
      protected ProcessHandler startProcess() throws ExecutionException {
        GeneralCommandLine commandLine =
            new GeneralCommandLine(getOptions().getScriptName());
        OSProcessHandler processHandler = ProcessHandlerFactory.getInstance()
            .createColoredProcessHandler(commandLine);
        ProcessTerminatedListener.attach(processHandler);
        return processHandler;
      }
    };
  }

}

```

# run_configuration/src/main/java/org/jetbrains/sdk/runConfiguration/DemoSettingsEditor.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.
package org.jetbrains.sdk.runConfiguration;

import com.intellij.openapi.fileChooser.FileChooserDescriptorFactory;
import com.intellij.openapi.options.SettingsEditor;
import com.intellij.openapi.ui.TextFieldWithBrowseButton;
import com.intellij.util.ui.FormBuilder;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

public class DemoSettingsEditor extends SettingsEditor<DemoRunConfiguration> {

  private final JPanel myPanel;
  private final TextFieldWithBrowseButton scriptPathField;

  public DemoSettingsEditor() {
    scriptPathField = new TextFieldWithBrowseButton();
    scriptPathField.addBrowseFolderListener("Select Script File", null, null,
        FileChooserDescriptorFactory.createSingleFileDescriptor());
    myPanel = FormBuilder.createFormBuilder()
        .addLabeledComponent("Script file", scriptPathField)
        .getPanel();
  }

  @Override
  protected void resetEditorFrom(DemoRunConfiguration demoRunConfiguration) {
    scriptPathField.setText(demoRunConfiguration.getScriptName());
  }

  @Override
  protected void applyEditorTo(@NotNull DemoRunConfiguration demoRunConfiguration) {
    demoRunConfiguration.setScriptName(scriptPathField.getText());
  }

  @NotNull
  @Override
  protected JComponent createEditor() {
    return myPanel;
  }

}

```

# run_configuration/src/main/java/org/jetbrains/sdk/runConfiguration/DemoRunConfigurationOptions.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.jetbrains.sdk.runConfiguration;

import com.intellij.execution.configurations.RunConfigurationOptions;
import com.intellij.openapi.components.StoredProperty;

public class DemoRunConfigurationOptions extends RunConfigurationOptions {

  private final StoredProperty<String> myScriptName =
      string("").provideDelegate(this, "scriptName");

  public String getScriptName() {
    return myScriptName.getValue(this);
  }

  public void setScriptName(String scriptName) {
    myScriptName.setValue(this, scriptName);
  }

}

```

# module/README.md
# Module Type Sample [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Project Wizard Tutorial in IntelliJ SDK Docs][docs:wizard]*

## Quickstart

The sample project that presents an implementation of the `com.intellij.moduleType` extension point, which adds a new module type to the *New Module* Project Wizard.
Module with a custom name, description, and icon set provides a `ModuleBuilder` with extra steps present for additional module configuration.

### Extension Points

| Name                      | Implementation                        | Extension Point Class |
|---------------------------|---------------------------------------|-----------------------|
| `com.intellij.moduleType` | [DemoModuleType][file:DemoModuleType] | `ModuleType`          |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:wizard]: https://plugins.jetbrains.com/docs/intellij/intro-project-wizard.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:DemoModuleType]: ./src/main/java/org/intellij/sdk/module/DemoModuleType.java


# module/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# module/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "module"

```

# module/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# module/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.module</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Module Type Sample</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.platform</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates example of working with module types<br>Adds <i>SDK Demo Module</i> to <b>File | New | Project...</b>
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin, change plugin ID</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <moduleType id="DEMO_MODULE_TYPE" implementationClass="org.intellij.sdk.module.DemoModuleType"/>
  </extensions>

</idea-plugin>

```

# module/src/main/java/org/intellij/sdk/module/DemoModuleWizardStep.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.module;

import com.intellij.ide.util.projectWizard.ModuleWizardStep;

import javax.swing.*;

public class DemoModuleWizardStep extends ModuleWizardStep {

  @Override
  public JComponent getComponent() {
    return new JLabel("Provide some setting here");
  }

  @Override
  public void updateDataModel() {
    //todo update model according to UI
  }

}

```

# module/src/main/java/org/intellij/sdk/module/DemoModuleBuilder.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.module;

import com.intellij.ide.util.projectWizard.ModuleBuilder;
import com.intellij.ide.util.projectWizard.ModuleWizardStep;
import com.intellij.ide.util.projectWizard.WizardContext;
import com.intellij.openapi.Disposable;
import com.intellij.openapi.module.ModuleType;
import com.intellij.openapi.roots.ModifiableRootModel;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class DemoModuleBuilder extends ModuleBuilder {

  @Override
  public void setupRootModel(@NotNull ModifiableRootModel model) {
  }

  @Override
  public ModuleType<DemoModuleBuilder> getModuleType() {
    return DemoModuleType.getInstance();
  }

  @Nullable
  @Override
  public ModuleWizardStep getCustomOptionsStep(WizardContext context, Disposable parentDisposable) {
    return new DemoModuleWizardStep();
  }

}

```

# module/src/main/java/org/intellij/sdk/module/DemoModuleType.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.module;

import com.intellij.ide.util.projectWizard.ModuleWizardStep;
import com.intellij.ide.util.projectWizard.WizardContext;
import com.intellij.openapi.module.ModuleType;
import com.intellij.openapi.module.ModuleTypeManager;
import com.intellij.openapi.roots.ui.configuration.ModulesProvider;
import icons.SdkIcons;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

final class DemoModuleType extends ModuleType<DemoModuleBuilder> {

  private static final String ID = "DEMO_MODULE_TYPE";

  DemoModuleType() {
    super(ID);
  }

  public static DemoModuleType getInstance() {
    return (DemoModuleType) ModuleTypeManager.getInstance().findByID(ID);
  }

  @NotNull
  @Override
  public DemoModuleBuilder createModuleBuilder() {
    return new DemoModuleBuilder();
  }

  @NotNull
  @Override
  public String getName() {
    return "SDK Module Type";
  }

  @NotNull
  @Override
  public String getDescription() {
    return "Example custom module type";
  }

  @NotNull
  @Override
  public Icon getNodeIcon(@Deprecated boolean b) {
    return SdkIcons.Sdk_default_icon;
  }

  @Override
  public ModuleWizardStep @NotNull [] createWizardSteps(@NotNull WizardContext wizardContext,
                                                        @NotNull DemoModuleBuilder moduleBuilder,
                                                        @NotNull ModulesProvider modulesProvider) {
    return super.createWizardSteps(wizardContext, moduleBuilder, modulesProvider);
  }

}

```

# module/src/main/java/icons/SdkIcons.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package icons;

import com.intellij.openapi.util.IconLoader;

import javax.swing.*;

public class SdkIcons {

  public static final Icon Sdk_default_icon = IconLoader.getIcon("/icons/sdk_16.svg", SdkIcons.class);

}

```

# comparing_string_references_inspection/README.md
# Comparing References Inspection Sample [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Code Inspections in IntelliJ SDK Docs][docs:code_inspections]*

## Quickstart

Comparing References Inspection Sample demonstrates the implementation of the [Code Inspections][docs:code_inspections] feature for Java classes.

The plugin inspects your Java code and highlights any fragments containing the comparison of two `String` variables.
If such a check finds a comparison using the `==` or !`=` operators instead of the `.equals()` method, the plugin proposes a *quick fix* action.

### Extension Points

| Name                           | Implementation                                                                  | Extension Point Class                 |
|--------------------------------|---------------------------------------------------------------------------------|---------------------------------------|
| `com.intellij.localInspection` | [ComparingStringReferencesInspection][file:ComparingStringReferencesInspection] | `AbstractBaseJavaLocalInspectionTool` |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:code_inspections]: https://plugins.jetbrains.com/docs/intellij/code-inspections.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:ComparingStringReferencesInspection]: ./src/main/java/org/intellij/sdk/codeInspection/ComparingStringReferencesInspection.java


# comparing_string_references_inspection/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

dependencies {
  testImplementation("junit:junit:4.13.2")
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
  plugins.set(listOf("com.intellij.java"))
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# comparing_string_references_inspection/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "comparing_string_references_inspection"

```

# comparing_string_references_inspection/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# comparing_string_references_inspection/src/test/testData/Eq.after.java
```java
public class Eq {
    public boolean compareStrings(String s1, String s2) {
        return (s1.equals(s2));
    }
}

```

# comparing_string_references_inspection/src/test/testData/Neq.after.java
```java
public class Neq {
  public boolean compareStrings(String s1, String s2) {
    return (!s1.equals(s2));
  }
}

```

# comparing_string_references_inspection/src/test/testData/Neq.java
```java
public class Neq {
  public boolean compareStrings(String s1, String s2) {
    return (s1 <caret>!= s2);
  }
}

```

# comparing_string_references_inspection/src/test/testData/Eq.java
```java
public class Eq {
    public boolean compareStrings(String s1, String s2) {
        return (<caret>s1 == s2);
    }
}

```

# comparing_string_references_inspection/src/test/java/org/intellij/sdk/codeInspection/ComparingStringReferencesInspectionTest.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.codeInspection;

import com.intellij.codeInsight.daemon.impl.HighlightInfo;
import com.intellij.codeInsight.intention.IntentionAction;
import com.intellij.testFramework.TestDataPath;
import com.intellij.testFramework.fixtures.LightJavaCodeInsightFixtureTestCase;
import org.jetbrains.annotations.NotNull;

import java.util.List;

@TestDataPath("$CONTENT_ROOT/testData")
public class ComparingStringReferencesInspectionTest extends LightJavaCodeInsightFixtureTestCase {

  private static final String QUICK_FIX_NAME =
      InspectionBundle.message("inspection.comparing.string.references.use.quickfix");

  @Override
  protected void setUp() throws Exception {
    super.setUp();
    myFixture.enableInspections(new ComparingStringReferencesInspection());
    // optimization: add a fake java.lang.String class to avoid loading all JDK classes for test
    myFixture.addClass("package java.lang; public final class String {}");
  }

  /**
   * Defines the path to files used for running tests.
   *
   * @return The path from this module's root directory ($MODULE_WORKING_DIR$) to the
   * directory containing files for these tests.
   */
  @Override
  protected String getTestDataPath() {
    return "src/test/testData";
  }

  /**
   * Test the '==' case.
   */
  public void testRelationalEq() {
    doTest("Eq");
  }

  /**
   * Test the '!=' case.
   */
  public void testRelationalNeq() {
    doTest("Neq");
  }

  /**
   * Given the name of a test file, runs comparing references inspection quick fix and tests
   * the results against a reference outcome file.
   * File name pattern 'foo.java' and 'foo.after.java' are matching before and after files
   * in the testData directory.
   *
   * @param testName test file name base
   */
  protected void doTest(@NotNull String testName) {
    // Initialize the test based on the testData file
    myFixture.configureByFile(testName + ".java");
    // Initialize the inspection and get a list of highlighted
    List<HighlightInfo> highlightInfos = myFixture.doHighlighting();
    assertFalse(highlightInfos.isEmpty());
    // Get the quick fix action for comparing references inspection and apply it to the file
    final IntentionAction action = myFixture.findSingleIntention(QUICK_FIX_NAME);
    assertNotNull(action);
    myFixture.launchAction(action);
    // Verify the results
    myFixture.checkResultByFile(testName + ".after.java");
  }

}

```

# comparing_string_references_inspection/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.codeInspection</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Comparing References Inspection Sample</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.platform</depends>
  <depends>com.intellij.java</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates implementing a Local Inspection Tool.<br> Adds entries to
      <b>Settings | Editor | Inspections | Java | Probable Bugs</b>.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin.</li>
        <li><b>1.1.0</b> Refactor resources, register this inspection.</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <!--
      Extend the IntelliJ Platform local inspection type and connect it to the implementation class in this plugin.
      <localInspection> type element is applied within the scope of a file under edit.
      It is preferred over <inspectionToolProvider>
      @see com.intellij.codeInspection.InspectionProfileEntry

      Attributes:
        - language - inspection language ID
        - shortName - not specified, will be computed by the underlying implementation classes
        - bundle - name of the message bundle for the "key" attribute
        - key - the key of the message to be shown in the Settings | Editor | Inspections panel
        - groupPath - defines the outermost grouping for this inspection in
            the Settings | Editor | Inspections panel. Not localized.
        - groupBundle - the name of a message bundle file to translate groupKey
            In this case, reuse an IntelliJ Platform bundle file from intellij.platform.resources.en
        - groupKey - the key to use for translation subgroup name using groupBundle file.
            In this case, reuse the IntelliJ Platform subcategory "Probable bugs"
        - enabledByDefault - inspection state when the Inspections panel is created.
        - level - the default level of error found by this inspection, e.g. INFO, ERROR, etc.
            @see com.intellij.codeHighlighting.HighlightDisplayLevel
        - implementationClass= the fully-qualified name of the inspection implementation class
    -->
    <localInspection language="JAVA"
                     bundle="messages.InspectionBundle"
                     key="inspection.comparing.string.references.display.name"
                     groupPath="Java"
                     groupBundle="messages.InspectionsBundle"
                     groupKey="group.names.probable.bugs"
                     enabledByDefault="true"
                     level="WARNING"
                     implementationClass="org.intellij.sdk.codeInspection.ComparingStringReferencesInspection"/>
  </extensions>

</idea-plugin>

```

# comparing_string_references_inspection/src/main/java/org/intellij/sdk/codeInspection/InspectionBundle.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.codeInspection;

import com.intellij.DynamicBundle;
import org.jetbrains.annotations.Nls;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.PropertyKey;

public final class InspectionBundle {

  @NonNls
  public static final String BUNDLE = "messages.InspectionBundle";

  private static final DynamicBundle ourInstance = new DynamicBundle(InspectionBundle.class, BUNDLE);

  private InspectionBundle() {
  }

  public static @Nls String message(@NotNull @PropertyKey(resourceBundle = BUNDLE) String key,
                                    Object @NotNull ... params) {
    return ourInstance.getMessage(key, params);
  }

}

```

# comparing_string_references_inspection/src/main/java/org/intellij/sdk/codeInspection/ComparingStringReferencesInspection.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.codeInspection;

import com.intellij.codeInspection.AbstractBaseJavaLocalInspectionTool;
import com.intellij.codeInspection.LocalQuickFix;
import com.intellij.codeInspection.ProblemDescriptor;
import com.intellij.codeInspection.ProblemsHolder;
import com.intellij.openapi.project.Project;
import com.intellij.psi.*;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.util.PsiTypesUtil;
import org.jetbrains.annotations.NotNull;

/**
 * Implements an inspection to detect when String references are compared using 'a==b' or 'a!=b'.
 * The quick fix converts these comparisons to 'a.equals(b) or '!a.equals(b)' respectively.
 */
final class ComparingStringReferencesInspection extends AbstractBaseJavaLocalInspectionTool {

  private final ReplaceWithEqualsQuickFix myQuickFix = new ReplaceWithEqualsQuickFix();

  /**
   * This method is overridden to provide a custom visitor
   * that inspects expressions with relational operators '==' and '!='.
   * The visitor must not be recursive and must be thread-safe.
   *
   * @param holder     object for the visitor to register problems found
   * @param isOnTheFly true if inspection was run in non-batch mode
   * @return non-null visitor for this inspection
   */
  @NotNull
  @Override
  public PsiElementVisitor buildVisitor(@NotNull final ProblemsHolder holder, boolean isOnTheFly) {
    return new JavaElementVisitor() {

      /**
       * Evaluate binary PSI expressions to see if they contain relational operators '==' and '!=',
       * AND they are of String type.
       * The evaluation ignores expressions comparing an object to null.
       * IF these criteria are met, register the problem in the ProblemsHolder.
       *
       * @param expression The binary expression to be evaluated.
       */
      @Override
      public void visitBinaryExpression(@NotNull PsiBinaryExpression expression) {
        super.visitBinaryExpression(expression);
        IElementType opSign = expression.getOperationTokenType();
        if (opSign == JavaTokenType.EQEQ || opSign == JavaTokenType.NE) {
          // The binary expression is the correct type for this inspection
          PsiExpression lOperand = expression.getLOperand();
          PsiExpression rOperand = expression.getROperand();
          if (rOperand == null || isNullLiteral(lOperand) || isNullLiteral(rOperand)) {
            return;
          }
          // Nothing is compared to null, now check the types being compared
          if (isStringType(lOperand) || isStringType(rOperand)) {
            // Identified an expression with potential problems, register problem with the quick fix object
            holder.registerProblem(expression,
                InspectionBundle.message("inspection.comparing.string.references.problem.descriptor"),
                myQuickFix);
          }
        }
      }

      private boolean isStringType(PsiExpression operand) {
        PsiClass psiClass = PsiTypesUtil.getPsiClass(operand.getType());
        if (psiClass == null) {
          return false;
        }

        return "java.lang.String".equals(psiClass.getQualifiedName());
      }

      private static boolean isNullLiteral(PsiExpression expression) {
        return expression instanceof PsiLiteralExpression &&
            ((PsiLiteralExpression) expression).getValue() == null;
      }
    };
  }

  /**
   * This class provides a solution to inspection problem expressions by manipulating the PSI tree to use 'a.equals(b)'
   * instead of '==' or '!='.
   */
  private static class ReplaceWithEqualsQuickFix implements LocalQuickFix {

    /**
     * Returns a partially localized string for the quick fix intention.
     * Used by the test code for this plugin.
     *
     * @return Quick fix short name.
     */
    @NotNull
    @Override
    public String getName() {
      return InspectionBundle.message("inspection.comparing.string.references.use.quickfix");
    }

    public void applyFix(@NotNull Project project, @NotNull ProblemDescriptor descriptor) {
      // binaryExpression holds a PSI expression of the form "x == y",
      // which needs to be replaced with "x.equals(y)"
      PsiBinaryExpression binaryExpression = (PsiBinaryExpression) descriptor.getPsiElement();
      IElementType opSign = binaryExpression.getOperationTokenType();
      PsiExpression lExpr = binaryExpression.getLOperand();
      PsiExpression rExpr = binaryExpression.getROperand();
      if (rExpr == null) {
        return;
      }
      // Step 1: Create a replacement fragment from text, with "a" and "b" as placeholders
      PsiElementFactory factory = JavaPsiFacade.getInstance(project).getElementFactory();
      PsiMethodCallExpression equalsCall =
          (PsiMethodCallExpression) factory.createExpressionFromText("a.equals(b)", null);
      // Step 2: Replace "a" and "b" with elements from the original file
      PsiExpression qualifierExpression =
          equalsCall.getMethodExpression().getQualifierExpression();
      assert qualifierExpression != null;
      qualifierExpression.replace(lExpr);
      equalsCall.getArgumentList().getExpressions()[0].replace(rExpr);
      // Step 3: Replace a larger element in the original file with the replacement tree
      PsiExpression result = (PsiExpression) binaryExpression.replace(equalsCall);

      // Steps 4-6 needed only for negation
      if (opSign == JavaTokenType.NE) {
        // Step 4: Create a replacement fragment with negation and negated operand placeholder
        PsiPrefixExpression negation =
            (PsiPrefixExpression) factory.createExpressionFromText("!a", null);
        PsiExpression operand = negation.getOperand();
        assert operand != null;
        // Step 5: Replace operand placeholder with the actual expression
        operand.replace(result);
        // Step 6: Replace the result with the negated expression
        result.replace(negation);
      }
    }

    @NotNull
    public String getFamilyName() {
      return getName();
    }

  }

}

```

# facet_basics/README.md
# Facet Basics [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Facet in IntelliJ SDK Docs][docs:facet_basics]*

## Quickstart

Facets extend base IDE features with additional frameworks support by providing additional libraries, dependencies, technologies, and UI elements for configuring framework-specific settings.

Facet Basics represents configuration specific for a particular framework or technology, associated with a module.
SDK Facet is available to use in the `Project Settings > Facets` section.
It allows us to specify any configuration specified by the `FacetConfiguration` implementation - path to the SDK in this case.

### Extension Points

| Name                     | Implementation                      | Extension Point Class |
|--------------------------|-------------------------------------|-----------------------|
| `com.intellij.facetType` | [DemoFacetType][file:DemoFacetType] | `FacetType`           |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:facet_basics]: https://plugins.jetbrains.com/docs/intellij/facet.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:DemoFacetType]: ./src/main/java/org/intellij/sdk/facet/DemoFacetType.java



# facet_basics/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# facet_basics/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "facet_basics"

```

# facet_basics/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# facet_basics/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.facet</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Facet Basics</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.lang</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates implementing the custom Facet pattern.<br>Adds <em>SDK Facet</em>
      to the Project Structure | Project Settings | Facets menu.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <b>2.1</b> Refactored for Gradle project format.<br>
      <b>2.0</b> Refactored to illustrate use of PersistentComponent.<br>
      <b>1.0</b> Release 2018.3 and earlier.
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <!-- Register the custom facet extension -->
    <facetType implementation="org.intellij.sdk.facet.DemoFacetType"/>
  </extensions>

</idea-plugin>

```

# facet_basics/src/main/java/org/intellij/sdk/facet/DemoFacetType.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.facet;

import com.intellij.facet.Facet;
import com.intellij.facet.FacetType;
import com.intellij.facet.FacetTypeId;
import com.intellij.openapi.module.Module;
import com.intellij.openapi.module.ModuleType;
import icons.SdkIcons;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

/**
 * Defines the type, id, and name of the {@link DemoFacet}.
 * Provides creation of {@link DemoFacet} and associated Configuration.
 * Allows application of this facet to all {@link ModuleType} instances.
 */
final class DemoFacetType extends FacetType<DemoFacet, DemoFacetConfiguration> {

  public static final String FACET_ID = "DEMO_FACET_ID";
  public static final String FACET_NAME = "SDK Facet";
  public static final FacetTypeId<DemoFacet> DEMO_FACET_TYPE_ID = new FacetTypeId<>(FACET_ID);

  public DemoFacetType() {
    super(DEMO_FACET_TYPE_ID, FACET_ID, FACET_NAME);
  }

  @Override
  public DemoFacetConfiguration createDefaultConfiguration() {
    return new DemoFacetConfiguration();
  }

  @Override
  public DemoFacet createFacet(@NotNull Module module,
                               String s,
                               @NotNull DemoFacetConfiguration configuration,
                               Facet facet) {
    return new DemoFacet(this, module, s, configuration, facet);
  }

  @Override
  public boolean isSuitableModuleType(final ModuleType type) {
    return true;
  }

  @Override
  public Icon getIcon() {
    return SdkIcons.Sdk_default_icon;
  }

}

```

# facet_basics/src/main/java/org/intellij/sdk/facet/DemoFacetConfiguration.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.facet;

import com.intellij.facet.FacetConfiguration;
import com.intellij.facet.ui.FacetEditorContext;
import com.intellij.facet.ui.FacetEditorTab;
import com.intellij.facet.ui.FacetValidatorsManager;
import com.intellij.openapi.components.PersistentStateComponent;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * Provides a custom implementation of the Configuration class for {@link DemoFacet}.
 */
public class DemoFacetConfiguration implements FacetConfiguration, PersistentStateComponent<DemoFacetState> {

  // Manages the data stored with this facet.
  private DemoFacetState myFacetState = new DemoFacetState();

  /**
   * Called by the IntelliJ Platform when saving this facet's state persistently.
   *
   * @return a component state. All properties, public and annotated fields are serialized.
   * Only values which differ from default (i.e. the value of newly instantiated class) are serialized.
   * {@code null} value indicates that the returned state won't be stored, and
   * as a result previously stored state will be used.
   */
  @Nullable
  @Override
  public DemoFacetState getState() {
    return myFacetState;
  }

  /**
   * Called by the IntelliJ Platform when this facet's state is loaded.
   * The method can and will be called several times, if config files were externally changed while IDEA running.
   */
  @Override
  public void loadState(@NotNull DemoFacetState state) {
    myFacetState = state;
  }

  /**
   * Creates a set of editor tabs for this facet, potentially one per context.
   *
   * @param context The context in which a facet is being added/deleted, or modified.
   * @param manager The manager which can be used to access custom validators.
   * @return Array of {@link DemoFacetEditorTab}. In this case size is always 1.
   */
  @Override
  public FacetEditorTab[] createEditorTabs(FacetEditorContext context, FacetValidatorsManager manager) {
    return new FacetEditorTab[]{
        new DemoFacetEditorTab(myFacetState, context, manager)
    };
  }

}

```

# facet_basics/src/main/java/org/intellij/sdk/facet/DemoFacetEditorTab.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.facet;

import com.intellij.facet.ui.FacetEditorContext;
import com.intellij.facet.ui.FacetEditorTab;
import com.intellij.facet.ui.FacetValidatorsManager;
import com.intellij.openapi.options.ConfigurationException;
import com.intellij.openapi.util.text.StringUtil;
import org.jetbrains.annotations.Nls;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;
import java.awt.*;

/**
 * Provides the JPanel to be displayed in the facet UI.
 * Manages validation and modification of the {@link DemoFacet} state.
 */
public class DemoFacetEditorTab extends FacetEditorTab {

  private static final String FACET_PANEL_PROMPT = "Path To SDK: ";

  private final DemoFacetState mySettings;
  private final JTextField myPath;

  /**
   * Only org.intellij.sdk.facet.DemoFacetState is captured so it can be updated per user changes in the EditorTab.
   *
   * @param state     {@link DemoFacetState} object persisting {@link DemoFacet} state.
   * @param context   Facet editor context, can be used to get e.g. the current project module.
   * @param validator Facet validator manager, can be used to get and apply a custom validator for this facet.
   */
  public DemoFacetEditorTab(@NotNull DemoFacetState state, @NotNull FacetEditorContext context,
                            @NotNull FacetValidatorsManager validator) {
    mySettings = state;
    myPath = new JTextField(state.getDemoFacetState());
  }

  /**
   * Provides the {@link JPanel} displayed in the Project Structure | Facet UI
   *
   * @return {@link JPanel} to be displayed in the {@link DemoFacetEditorTab}.
   */
  @NotNull
  @Override
  public JComponent createComponent() {
    JPanel top = new JPanel(new BorderLayout());
    top.add(new JLabel(FACET_PANEL_PROMPT), BorderLayout.WEST);
    top.add(myPath);
    JPanel facetPanel = new JPanel(new BorderLayout());
    facetPanel.add(top, BorderLayout.NORTH);
    return facetPanel;
  }

  /**
   * @return the name of this facet for display in this editor tab.
   */
  @Override
  @Nls(capitalization = Nls.Capitalization.Title)
  public String getDisplayName() {
    return DemoFacetType.FACET_NAME;
  }

  /**
   * Determines if the facet state entered in the UI differs from the currently stored state.
   * Called when user changes text in {@link #myPath}.
   *
   * @return {@code true} if the state returned from the panel's UI differs from the stored facet state.
   */
  @Override
  public boolean isModified() {
    return !StringUtil.equals(mySettings.getDemoFacetState(), myPath.getText().trim());
  }

  /**
   * Stores new facet state (text) entered by the user.
   * Called when {@link #isModified()} returns true.
   *
   * @throws ConfigurationException if anything generates an exception.
   */
  @Override
  public void apply() throws ConfigurationException {
    // Not much to go wrong here, but fulfill the contract
    try {
      String newTextContent = myPath.getText();
      mySettings.setDemoFacetState(newTextContent);
    } catch (Exception e) {
      throw new ConfigurationException(e.toString());
    }
  }

  /**
   * Copies current {@link DemoFacetState} into the {@link #myPath} UI element.
   * This method is called each time this editor tab is needed for display.
   */
  @Override
  public void reset() {
    myPath.setText(mySettings.getDemoFacetState());
  }

}

```

# facet_basics/src/main/java/org/intellij/sdk/facet/DemoFacetState.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.facet;

import org.jetbrains.annotations.NotNull;

/**
 * A simple class to store state for the {@link DemoFacet}.
 * In this case it is just a string containing a path to an SDK.
 */
public class DemoFacetState {

  static final String DEMO_FACET_INIT_PATH = "";

  public String myPathToSdk;

  DemoFacetState() {
    setDemoFacetState(DEMO_FACET_INIT_PATH);
  }

  @NotNull
  public String getDemoFacetState() {
    return myPathToSdk;
  }

  public void setDemoFacetState(@NotNull String newPath) {
    myPathToSdk = newPath;
  }

}

```

# facet_basics/src/main/java/org/intellij/sdk/facet/DemoFacet.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.facet;

import com.intellij.facet.Facet;
import com.intellij.facet.FacetType;
import com.intellij.openapi.module.Module;

/**
 * Demo Facet class. Everything is handled by the super class.
 */
public class DemoFacet extends Facet<DemoFacetConfiguration> {

  public DemoFacet(FacetType facetType,
                   Module module,
                   String name,
                   DemoFacetConfiguration configuration,
                   Facet underlyingFacet) {
    super(facetType, module, name, configuration, underlyingFacet);
  }

}

```

# facet_basics/src/main/java/icons/SdkIcons.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package icons;

import com.intellij.openapi.util.IconLoader;

import javax.swing.*;

public class SdkIcons {

  public static final Icon Sdk_default_icon = IconLoader.getIcon("/icons/sdk_16.svg", SdkIcons.class);

}

```

# project_wizard/README.md
# Project Wizard Demo [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Project Wizard in IntelliJ SDK Docs][docs:project_wizard]*

## Quickstart

This demo project shows how to add an extra step to the Project Wizard to provide additional project configuration settings.
The new step contains a simple `JLabel` element as an example presentation of the new step content.

### Extension Points

| Name                         | Implementation                                    | Extension Point Class |
|------------------------------|---------------------------------------------------|-----------------------|
| `com.intellij.moduleBuilder` | [DemoModuleWizardStep][file:DemoModuleWizardStep] | `ModuleBuilder`       |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:project_wizard]: https://plugins.jetbrains.com/docs/intellij/intro-project-wizard.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:DemoModuleWizardStep]: ./src/main/java/org/intellij/sdk/project/wizard/DemoModuleWizardStep.java


# project_wizard/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# project_wizard/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "project_wizard"

```

# project_wizard/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# project_wizard/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.project.wizard</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Project Wizard Demo</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.platform</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates working with the Project Wizard.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <moduleBuilder builderClass="org.intellij.sdk.project.wizard.DemoModuleWizardStep"
                   id="DEMO_STEP"
                   order="first"/>
  </extensions>

</idea-plugin>

```

# project_wizard/src/main/java/org/intellij/sdk/project/wizard/DemoModuleWizardStep.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.project.wizard;

import com.intellij.ide.util.projectWizard.ModuleBuilder;
import com.intellij.ide.util.projectWizard.ModuleWizardStep;
import com.intellij.ide.util.projectWizard.WizardContext;
import com.intellij.openapi.module.ModuleType;
import com.intellij.openapi.roots.ModifiableRootModel;
import com.intellij.openapi.roots.ui.configuration.ModulesProvider;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

final class DemoModuleWizardStep extends ModuleBuilder {

  public void setupRootModel(@NotNull ModifiableRootModel modifiableRootModel) {
  }

  public ModuleType<?> getModuleType() {
    return ModuleType.EMPTY; //or it could be other module type
  }

  @Override
  public ModuleWizardStep[] createWizardSteps(@NotNull WizardContext wizardContext,
                                              @NotNull ModulesProvider modulesProvider) {
    return new ModuleWizardStep[]{new ModuleWizardStep() {
      @Override
      public JComponent getComponent() {
        return new JLabel("Put your content here");
      }

      @Override
      public void updateDataModel() {

      }
    }};
  }

}

```

# action_basics/README.md
# Action Basics Sample Project [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Action System in IntelliJ SDK Docs][docs:actions]*

## Quickstart

The Action Basics Sample Project demonstrates the process of registering actions in various configurations.
Each action is an extension of the `AnAction` abstract class and brings the possibility of extending the IDE with an event performed with the user interaction - i.e., clicking the button, using the keyboard or mouse shortcuts.

This Plugin registers the [`PopupDialogAction`][file:PopupDialogAction] action, which provides a popup dialog as feedback, in three different ways:
- by assigning the keyboard (<kbd>Ctrl/Cmd</kbd>+<kbd>Alt</kbd>+<kbd>A</kbd>, <kbd>C</kbd>) and mouse shortcuts (<kbd>Ctrl/Cmd</kbd> + <kbd>Mouse Button 3</kbd> + <kbd>Double Click</kbd>),
- by adding an action to the `ToolsMenu` directly, and as part of new groups added to the Tools menu,
- by adding an action to a new group in the `EditorPopupMenu`, which is the Editor's context menu.

Additional features of the plugin:
- [Using the `<override-text>`][docs:action-override] element in an [`<action>`][docs:plugin-configuration-file:actions:action] element is demonstrated in the `plugin.xml` declaration to add the `PopupDialogAction` action directly to the `ToolsMenu`.
- [Localization of action and group][docs:action-locale] `text` and `description` attributes using a [`<resource-bundle>`][docs:plugin-configuration-file:resource-bundle] is demonstrated in the declaration to add a new group to the `EditorPopupMenu`.

### Actions

| ID                                                 | Implementation                                            | Base Action Class |
|----------------------------------------------------|-----------------------------------------------------------|-------------------|
| `org.intellij.sdk.action.GroupPopDialogAction`     | [PopupDialogAction][file:PopupDialogAction]               | `AnAction`        |
| `org.intellij.sdk.action.PopupDialogAction`        | [PopupDialogAction][file:PopupDialogAction]               | `AnAction`        |
| `org.intellij.sdk.action.CustomGroupedAction`      | [PopupDialogAction][file:PopupDialogAction]               | `AnAction`        |
| `org.intellij.sdk.action.CustomDefaultActionGroup` | [CustomDefaultActionGroup][file:CustomDefaultActionGroup] | `ActionGroup`     |
| `org.intellij.sdk.action.DynamicActionGroup`       | [DynamicActionGroup][file:DynamicActionGroup]             | `ActionGroup`     |

*Reference: [Action System in IntelliJ SDK Docs][docs:actions]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:actions]: https://plugins.jetbrains.com/docs/intellij/basic-action-system.html
[docs:action-override]: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html#idea-plugin__actions__action__override-text
[docs:action-locale]: https://plugins.jetbrains.com/docs/intellij/basic-action-system.html#localizing-actions-and-groups
[docs:plugin-configuration-file:actions:action]: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html#idea-plugin__actions__action
[docs:plugin-configuration-file:resource-bundle]: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html#idea-plugin__resource-bundle

[file:PopupDialogAction]: ./src/main/java/org/intellij/sdk/action/PopupDialogAction.java
[file:CustomDefaultActionGroup]: ./src/main/java/org/intellij/sdk/action/CustomDefaultActionGroup.java
[file:DynamicActionGroup]: ./src/main/java/org/intellij/sdk/action/DynamicActionGroup.java


# action_basics/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# action_basics/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "action_basics"

```

# action_basics/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# action_basics/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.action</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Action Sample</name>

  <!-- Indicate this plugin can be loaded in all IntelliJ Platform-based products. -->
  <depends>com.intellij.modules.platform</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates implementing Action and Action Group patterns.<br> Adds entries to the Tools menu.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Renamed from register_actions and converted to Gradle project.</li>
        <li><b>1.1</b> Refactor to give users feedback when selecting menu items.</li>
        <li><b>1.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <!-- Declare the default resource location for localizing menu strings -->
  <resource-bundle>messages.BasicActionsBundle</resource-bundle>

  <actions>
    <!--
      See https://plugins.jetbrains.com/docs/intellij/basic-action-system.html#registering-actions
      for information about the elements and attributes used for actions and groups.

      This <action> element adds a static menu item in first position of the Tools menu that shows PopupDialogAction.
      Note this element has no text or description attributes because translations for them are given
      by action-id in the resource-bundle.
      An <override-text> element is also used for demonstration purposes to show alternate text and description strings
      for this action's entries in the MainMenu. (Which includes the ToolsMenu. Try commenting out the override-text
      element and see how the menu text changes.) The alternate text and description attributes do not
      appear here because they are defined by action-id in the resource-bundle.
    -->
    <action id="org.intellij.sdk.action.PopupDialogAction" class="org.intellij.sdk.action.PopupDialogAction"
            text="Action Basics Plugin: Pop Dialog Action" description="SDK action example"
            icon="SdkIcons.Sdk_default_icon">
      <add-to-group group-id="ToolsMenu" anchor="first"/>
      <override-text place="MainMenu" text="Pop Dialog Action"/>
      <keyboard-shortcut first-keystroke="control alt A" second-keystroke="C" keymap="$default"/>
      <mouse-shortcut keystroke="control button3 doubleClick" keymap="$default"/>
    </action>
    <!--
      All of the following menu groups add the action PopupDialogAction to menus in different ways.
      Note that even though these groups reuse the same action class, in each use the action ids are unique.

      GroupedActions demonstrates declaring an action group using the default ActionGroup implementation provided by the
      IntelliJ Platform framework. (Note the lack of a group "class" attribute.) GroupedActions gets inserted after
      PopupDialogAction in the Tools menu. Because the group's implementation is default, it cannot impose
      enable/disable conditions. Instead it must rely on the conditions imposed by the parent menu where it is inserted.
      It declares one action in the group.
    -->
    <group id="org.intellij.sdk.action.GroupedActions"
           text="Static Grouped Actions" description="SDK statically grouped action example"
           popup="true" icon="SdkIcons.Sdk_default_icon">
      <add-to-group group-id="ToolsMenu" anchor="after" relative-to-action="org.intellij.sdk.action.PopupDialogAction"/>
      <action id="org.intellij.sdk.action.GroupPopDialogAction" class="org.intellij.sdk.action.PopupDialogAction"
              text="A Group Action" description="SDK static grouped action example"
              icon="SdkIcons.Sdk_default_icon">
      </action>
    </group>
    <!--
      CustomDefaultActionGroup demonstrates declaring an action group based on a ActionGroup class supplied by this
      plugin. This group is to be inserted atop the Editor Popup Menu. It declares one action in the group.
      The group and action implementations are internationalized, so their declarations do not use the text or
      description attributes. Instead, the information is defined in the BasicActionsBundle.
    -->
    <group id="org.intellij.sdk.action.CustomDefaultActionGroup"
           class="org.intellij.sdk.action.CustomDefaultActionGroup"
           popup="true">
      <add-to-group group-id="EditorPopupMenu" anchor="first"/>
      <action id="org.intellij.sdk.action.CustomGroupedAction" class="org.intellij.sdk.action.PopupDialogAction"
              icon="SdkIcons.Sdk_default_icon"/>
    </group>
    <!--
      DynamicActionGroup demonstrates declaring an action group without a static action declaration.
      An action is added to the group programmatically in the DynamicActionGroup implementation.
    -->
    <group id="org.intellij.sdk.action.DynamicActionGroup" class="org.intellij.sdk.action.DynamicActionGroup"
           popup="true" text="Dynamically Grouped Actions" description="SDK dynamically grouped action example"
           icon="SdkIcons.Sdk_default_icon">
      <add-to-group group-id="ToolsMenu" anchor="after" relative-to-action="org.intellij.sdk.action.GroupedActions"/>
    </group>
  </actions>

</idea-plugin>

```

# action_basics/src/main/java/org/intellij/sdk/action/PopupDialogAction.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.action;

import com.intellij.openapi.actionSystem.ActionUpdateThread;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.Messages;
import com.intellij.pom.Navigatable;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

/**
 * Action class to demonstrate how to interact with the IntelliJ Platform.
 * The only action this class performs is to provide the user with a popup dialog as feedback.
 * Typically, this class is instantiated by the IntelliJ Platform framework based on declarations
 * in the plugin.xml file.
 * But when added at runtime, this class is instantiated by an action group.
 */
public class PopupDialogAction extends AnAction {

  @Override
  public @NotNull ActionUpdateThread getActionUpdateThread() {
    return ActionUpdateThread.BGT;
  }

  /**
   * This default constructor is used by the IntelliJ Platform framework to instantiate this class based on plugin.xml
   * declarations. Only needed in {@link PopupDialogAction} class because a second constructor is overridden.
   */
  public PopupDialogAction() {
    super();
  }

  /**
   * This constructor is used to support dynamically added menu actions.
   * It sets the text, description to be displayed for the menu item.
   * Otherwise, the default AnAction constructor is used by the IntelliJ Platform.
   *
   * @param text        The text to be displayed as a menu item.
   * @param description The description of the menu item.
   * @param icon        The icon to be used with the menu item.
   */
  @SuppressWarnings("ActionPresentationInstantiatedInCtor") // via DynamicActionGroup
  public PopupDialogAction(@Nullable String text, @Nullable String description, @Nullable Icon icon) {
    super(text, description, icon);
  }

  @Override
  public void actionPerformed(@NotNull AnActionEvent event) {
    // Using the event, create and show a dialog
    Project currentProject = event.getProject();
    StringBuilder message =
        new StringBuilder(event.getPresentation().getText() + " Selected!");
    // If an element is selected in the editor, add info about it.
    Navigatable selectedElement = event.getData(CommonDataKeys.NAVIGATABLE);
    if (selectedElement != null) {
      message.append("\nSelected Element: ").append(selectedElement);
    }
    String title = event.getPresentation().getDescription();
    Messages.showMessageDialog(
        currentProject,
        message.toString(),
        title,
        Messages.getInformationIcon());
  }

  @Override
  public void update(AnActionEvent e) {
    // Set the availability based on whether a project is open
    Project project = e.getProject();
    e.getPresentation().setEnabledAndVisible(project != null);
  }

}

```

# action_basics/src/main/java/org/intellij/sdk/action/DynamicActionGroup.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.action;

import com.intellij.openapi.actionSystem.ActionGroup;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import icons.SdkIcons;
import org.jetbrains.annotations.NotNull;

/**
 * Demonstrates adding an action group to a menu statically in plugin.xml, and then creating a menu item within
 * the group at runtime. See plugin.xml for the declaration of {@link DynamicActionGroup}, and note the group
 * declaration does not contain an action. {@link DynamicActionGroup} is based on {@link ActionGroup} because menu
 * children are determined on rules other than just positional constraints.
 */
public class DynamicActionGroup extends ActionGroup {

  /**
   * Returns an array of menu actions for the group.
   *
   * @param e Event received when the associated group-id menu is chosen.
   * @return AnAction[] An instance of {@link AnAction}, in this case containing a single instance of the
   * {@link PopupDialogAction} class.
   */
  @Override
  public AnAction @NotNull [] getChildren(AnActionEvent e) {
    return new AnAction[]{
            new PopupDialogAction("Action Added at Runtime", "Dynamic Action Demo", SdkIcons.Sdk_default_icon)
    };
  }

}

```

# action_basics/src/main/java/org/intellij/sdk/action/CustomDefaultActionGroup.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.action;

import com.intellij.openapi.actionSystem.ActionUpdateThread;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.actionSystem.DefaultActionGroup;
import com.intellij.openapi.editor.Editor;
import icons.SdkIcons;
import org.jetbrains.annotations.NotNull;

/**
 * Creates an action group to contain menu actions. See plugin.xml declarations.
 */
public class CustomDefaultActionGroup extends DefaultActionGroup {

  @Override
  public @NotNull ActionUpdateThread getActionUpdateThread() {
    return ActionUpdateThread.BGT;
  }

  /**
   * Given {@link CustomDefaultActionGroup} is derived from {@link com.intellij.openapi.actionSystem.ActionGroup},
   * in this context {@code update()} determines whether the action group itself should be enabled or disabled.
   * Requires an editor to be active in order to enable the group functionality.
   *
   * @param event Event received when the associated group-id menu is chosen.
   */
  @Override
  public void update(AnActionEvent event) {
    // Enable/disable depending on whether user is editing
    Editor editor = event.getData(CommonDataKeys.EDITOR);
    event.getPresentation().setEnabled(editor != null);
    // Take this opportunity to set an icon for the group.
    event.getPresentation().setIcon(SdkIcons.Sdk_default_icon);
  }

}

```

# action_basics/src/main/java/icons/SdkIcons.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package icons;

import com.intellij.openapi.util.IconLoader;

import javax.swing.*;

public class SdkIcons {

  public static final Icon Sdk_default_icon = IconLoader.getIcon("/icons/sdk_16.svg", SdkIcons.class);

}

```

# _gradleCompositeBuild/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

// Composite Build for all SDK Code Sample projects (excluding those under /product_specific/ to reduce dependencies)

rootProject.name = "SDK Code Samples"

includeBuild("../action_basics")
includeBuild("../comparing_string_references_inspection")
includeBuild("../conditional_operator_intention")
includeBuild("../editor_basics")
includeBuild("../facet_basics")
includeBuild("../framework_basics")
includeBuild("../live_templates")
includeBuild("../max_opened_projects")
includeBuild("../module")
includeBuild("../project_model")
includeBuild("../project_view_pane")
includeBuild("../project_wizard")
includeBuild("../psi_demo")
includeBuild("../run_configuration")
includeBuild("../settings")
includeBuild("../simple_language_plugin")
includeBuild("../tool_window")
includeBuild("../tree_structure_provider")

```

# psi_demo/README.md
# PSI Demo [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Navigating the PSI in IntelliJ SDK Docs][docs:navigating_psi]*

## Quickstart

PSI Demo project demonstrates working with the PSI Navigation by implementing `AnAction` that through the message dialog, informs about:
- an element at the caret,
- containing method,
- containing class,
- local variables.

### Actions

| ID                  | Implementation                                          | Base Action Class |
|---------------------|---------------------------------------------------------|-------------------|
| `PsiNavigationDemo` | [PsiNavigationDemoAction][file:PsiNavigationDemoAction] | `AnAction`        |

*Reference: [Action System in IntelliJ SDK Docs][docs:actions]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:actions]: https://plugins.jetbrains.com/docs/intellij/basic-action-system.html
[docs:navigating_psi]: https://plugins.jetbrains.com/docs/intellij/navigating-psi.html

[file:PsiNavigationDemoAction]: ./src/main/java/org/intellij/sdk/psi/PsiNavigationDemoAction.java


# psi_demo/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
  plugins.set(listOf("com.intellij.java"))
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# psi_demo/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "psi_demo"

```

# psi_demo/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# psi_demo/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.psi</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: PSI Demo</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.platform</depends>
  <depends>com.intellij.java</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates working with the PSI Navigation.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <actions>
    <action class="org.intellij.sdk.psi.PsiNavigationDemoAction" id="PsiNavigationDemo"
            text="PSI Navigation Demo...">
      <add-to-group group-id="ToolsMenu" anchor="last"/>
    </action>
  </actions>

</idea-plugin>

```

# psi_demo/src/main/java/org/intellij/sdk/psi/PsiNavigationDemoAction.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.psi;

import com.intellij.openapi.actionSystem.ActionUpdateThread;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.ui.Messages;
import com.intellij.psi.*;
import com.intellij.psi.util.PsiTreeUtil;
import org.jetbrains.annotations.NotNull;

public class PsiNavigationDemoAction extends AnAction {

  @Override
  public @NotNull ActionUpdateThread getActionUpdateThread() {
    return ActionUpdateThread.BGT;
  }

  @Override
  public void actionPerformed(AnActionEvent anActionEvent) {
    Editor editor = anActionEvent.getData(CommonDataKeys.EDITOR);
    PsiFile psiFile = anActionEvent.getData(CommonDataKeys.PSI_FILE);
    if (editor == null || psiFile == null) {
      return;
    }
    int offset = editor.getCaretModel().getOffset();

    final StringBuilder infoBuilder = new StringBuilder();
    PsiElement element = psiFile.findElementAt(offset);
    infoBuilder.append("Element at caret: ").append(element).append("\n");
    if (element != null) {
      PsiMethod containingMethod = PsiTreeUtil.getParentOfType(element, PsiMethod.class);
      infoBuilder
          .append("Containing method: ")
          .append(containingMethod != null ? containingMethod.getName() : "none")
          .append("\n");
      if (containingMethod != null) {
        PsiClass containingClass = containingMethod.getContainingClass();
        infoBuilder
            .append("Containing class: ")
            .append(containingClass != null ? containingClass.getName() : "none")
            .append("\n");

        infoBuilder.append("Local variables:\n");
        containingMethod.accept(new JavaRecursiveElementVisitor() {
          @Override
          public void visitLocalVariable(@NotNull PsiLocalVariable variable) {
            super.visitLocalVariable(variable);
            infoBuilder.append(variable.getName()).append("\n");
          }
        });
      }
    }
    Messages.showMessageDialog(anActionEvent.getProject(), infoBuilder.toString(), "PSI Info", null);
  }

  @Override
  public void update(AnActionEvent e) {
    Editor editor = e.getData(CommonDataKeys.EDITOR);
    PsiFile psiFile = e.getData(CommonDataKeys.PSI_FILE);
    e.getPresentation().setEnabled(editor != null && psiFile != null);
  }

}

```

# SAMPLE_README.md
# Sample [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Sample Article in IntelliJ SDK Docs][docs:sampleArticle]*

## Quickstart

The Sample implements `com.intellij.sample` Extension Point, which should be explained properly in this Quickstart section.

### Extension Points

| Name                  | Implementation                                    | Extension Point Class |
|-----------------------|---------------------------------------------------|-----------------------|
| `com.intellij.sample` | [SampleExtensionPoint][file:SampleExtensionPoint] | `ExtensionPoint`      |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*

### Actions

| ID                                     | Implementation                    | Base Action Class |
|----------------------------------------|-----------------------------------|-------------------|
| `org.intellij.sdk.action.SampleAction` | [SampleAction][file:SampleAction] | `AnAction`        |

*Reference: [Action System in IntelliJ SDK Docs][docs:actions]*

### Listeners

| Name     | Implementation                        | Listener Class |
|----------|---------------------------------------|----------------|
| listener | [SampleListener][file:SampleListener] | `Listener`     |

*Reference: [Plugin Listeners in IntelliJ SDK Docs][docs:listeners]*

[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:actions]: https://plugins.jetbrains.com/docs/intellij/basic-action-system.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html
[docs:listeners]: https://plugins.jetbrains.com/docs/intellij/plugin-listeners.html
[docs:sampleArticle]: https://plugins.jetbrains.com/docs/intellij/sampleArticle.html

[file:SampleExtensionPoint]: ./src/main/java/org/intellij/sdk/sample/SampleExtensionPoint.java
[file:SampleAction]: ./src/main/java/org/intellij/sdk/sample/SampleAction.java
[file:SampleListener]: ./src/main/java/org/intellij/sdk/sample/SampleListener.java


# README.md
# IntelliJ Platform SDK Code Samples

[![official JetBrains project](https://jb.gg/badges/official-flat-square.svg)][jb:github]
[![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg?style=flat-square)][jb:docs]
[![X Follow](https://img.shields.io/badge/follow-%40JBPlatform-1DA1F2?logo=x)][jb:x]
[![Build](https://img.shields.io/github/actions/workflow/status/JetBrains/intellij-sdk-docs/code-samples.yml?branch=main&style=flat-square)][gh:workflow-code-samples]
[![Slack](https://img.shields.io/badge/Slack-%23intellij--platform-blue?style=flat-square&logo=Slack)][jb:slack]

Learn how to build plugins using IntelliJ Platform SDK for the [JetBrains products][jb:products] by experimenting with our code samples.
These samples show you how features work and help you jumpstart your plugins.

> [!TIP]
> To start a new plugin project, consider using [IntelliJ Platform Plugin Template][gh:template] which offers a pure boilerplate template to make it easier to create a new plugin project.
>
> The code samples can also be found in the [IntelliJ SDK Code Samples](https://github.com/JetBrains/intellij-sdk-code-samples) mirror repository.

To learn more, browse [available Extension Points][docs:eps], explore Extension Point usages in open-source plugins using [IntelliJ Platform Explorer](https://jb.gg/ipe) and learn how to [Explore the IntelliJ Platform API][docs:explore-api].

## Target Platform

All Code Samples target the latest GA platform release.
Previous releases are made available via [tags](https://github.com/JetBrains/intellij-sdk-code-samples/tags).

## Structure

Code Samples depend on the [IntelliJ Platform SDK][docs] and [Gradle][docs:gradle] as a build system.

The main plugin definition file is stored in the `plugin.xml` file, which is created according to the [Plugin Configuration File documentation][docs:plugin.xml].
It describes definitions of the actions, extensions, or listeners provided by the plugin.

## Code Samples

Please see [Code Samples][docs:code-samples] topic on how to import and run code samples.

In the following table, you may find all available samples provided in the separated directories as stand-alone projects available for running with the Gradle `runIde` task.

| Code Sample                                                                 | Description                                                                                                                                                       |
|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Action Basics](./action_basics)                                            | Action and Action Group patterns implementation, adds entries to the Tools menu.                                                                                  |
| [Comparing References Inspection](./comparing_string_references_inspection) | Local Inspection Tool, adds entries to **Settings &#124; Editor &#124; Inspections &#124; Java &#124; Probable Bugs**.                                            |
| [Conditional Operator Intention](./conditional_operator_intention)          | Intention action, suggests converting a ternary operator into an `if` block and adds entry to **Settings &#124; Editor &#124; Intentions &#124; SDK Intentions**. |
| [Editor Basics](./editor_basics)                                            | Basic Editor APIs example with editor popup menu with extra actions.                                                                                              |
| [Framework Basics](./framework_basics)                                      | Basic *SDK Demo Framework* support added to the **File &#124; New &#124; Project &#124; Java** wizard.                                                            |
| [Kotlin Demo](./kotlin_demo)                                                | Kotlin example extending the *Main Menu* with a **Greeting** menu group.                                                                                          |
| [Live Templates](./live_templates)                                          | Live templates for Markdown language, adds an entry to the **Settings &#124; Editor &#124; Live Templates** dialog.                                               |
| [Max Opened Projects](./max_opened_projects)                                | Application services and listeners, shows warning dialog when more than 3 open projects are opened.                                                               |
| [Module](./module)                                                          | *SDK Demo Module* module type added to the **File &#124; New &#124; Project...** wizard.                                                                          |
| [Product Specific - PyCharm Sample](./product_specific/pycharm_basics)      | Plugin project configuration for the PyCharm IDE.                                                                                                                 |
| [Project Model](./project_model)                                            | Interacts with the project model, adds menu items to **Tools** and **Editor Context** menus.                                                                      |
| [Project View Pane](./project_view_pane)                                    | Project View Pane listing only image files.                                                                                                                       |
| [Project Wizard](./project_wizard)                                          | Project Wizard example with demo steps.                                                                                                                           |
| [PSI Demo](./psi_demo)                                                      | PSI Navigation features presentation.                                                                                                                             |
| [Run Configuration](./run_configuration)                                    | Run configuration implementation with factory, options and UI.                                                                                                    |
| [Settings](./settings)                                                      | Custom settings panel, adds a settings panel to the **Settings** panel under **Tools**.                                                                           |
| [Simple Language Plugin](./simple_language_plugin)                          | Custom language support, defines a new *Simple language* with syntax highlighting, annotations, code completion, and other features.                              |
| [Theme Basics](./theme_basics)                                              | Sample *theme* plugin with basic interface modifications.                                                                                                         |
| [Tool Window](./tool_window)                                                | Custom Tool Window example plugin.                                                                                                                                |
| [Tree Structure Provider](./tree_structure_provider)                        | Tree Structure Provider showing only plain text files.                                                                                                            |

[gh:workflow-code-samples]: https://github.com/JetBrains/intellij-sdk-docs/actions/workflows/code-samples.yml
[gh:template]: https://github.com/JetBrains/intellij-platform-plugin-template

[jb:github]: https://github.com/JetBrains/.github/blob/main/profile/README.md
[jb:docs]: https://plugins.jetbrains.com/docs/intellij/
[jb:products]: https://www.jetbrains.com/products.html
[jb:slack]: https://plugins.jetbrains.com/slack
[jb:x]: https://x.com/JBPlatform

[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:code-samples]: https://plugins.jetbrains.com/docs/intellij/code-samples.html
[docs:eps]: https://plugins.jetbrains.com/docs/intellij/extension-point-list.html
[docs:gradle]: https://plugins.jetbrains.com/docs/intellij/developing-plugins.html
[docs:plugin.xml]: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html
[docs:explore-api]: https://plugins.jetbrains.com/docs/intellij/explore-api.html


# editor_basics/README.md
# Editor Sample Project [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Basics of Working with the Editor in IntelliJ SDK Docs][docs:editor_basics]*

## Quickstart

Editor Sample Project provides a `TypedHandlerDelegate` implementation, which inserts `editor_basics` on the top of the edited document any time user types a character.
In addition, three actions are available in the Editor context menu:

- Editor Replace Text - replaces the selected text with `editor_basics`,
- Editor Add Caret - adds extra caret below the current one,
- Caret Position - shows message dialog with information about the caret position.

### Extension Points

| Name                        | Implementation                        | Extension Point Class  |
|-----------------------------|---------------------------------------|------------------------|
| `com.intellij.typedHandler` | [MyTypedHandler][file:MyTypedHandler] | `TypedHandlerDelegate` |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*

### Actions

| ID                                         | Implementation                                              | Base Action Class |
|--------------------------------------------|-------------------------------------------------------------|-------------------|
| `EditorBasics.EditorIllustrationAction`    | [EditorIllustrationAction][file:EditorIllustrationAction]   | `AnAction`        |
| `EditorBasics.EditorHandlerIllustration`   | [EditorHandlerIllustration][file:EditorHandlerIllustration] | `AnAction`        |
| `EditorBasics.LogicalPositionIllustration` | [EditorAreaIllustration][file:EditorAreaIllustration]       | `AnAction`        |

*Reference: [Action System in IntelliJ SDK Docs][docs:actions]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:actions]: https://plugins.jetbrains.com/docs/intellij/basic-action-system.html
[docs:editor_basics]: https://plugins.jetbrains.com/docs/intellij/editor-basics.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:MyTypedHandler]: ./src/main/java/org/intellij/sdk/editor/MyTypedHandler.java
[file:EditorIllustrationAction]: ./src/main/java/org/intellij/sdk/editor/EditorIllustrationAction.java
[file:EditorHandlerIllustration]: ./src/main/java/org/intellij/sdk/editor/EditorHandlerIllustration.java
[file:EditorAreaIllustration]: ./src/main/java/org/intellij/sdk/editor/EditorAreaIllustration.java


# editor_basics/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# editor_basics/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "editor_basics"

```

# editor_basics/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# editor_basics/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.editor</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Editor Sample</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.platform</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Illustrates various basic Editor APIs. Requires at least project to be open, and a file open in the editor
      to see the menu items this plugin adds to the editor popup menu.<br>Mouse over each of this plugin's menu items
      to see hints in the lower left corner of the IDE.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin</li>
        <li><b>1.0.0</b> Release 2019.1 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <actions>
    <action id="EditorBasics.EditorIllustrationAction"
            class="org.intellij.sdk.editor.EditorIllustrationAction"
            text="Editor Replace Text"
            description="Replaces selected text with 'Replacement'."
            icon="SdkIcons.Sdk_default_icon">
      <add-to-group group-id="EditorPopupMenu" anchor="first"/>
    </action>
    <action id="EditorBasics.EditorHandlerIllustration"
            class="org.intellij.sdk.editor.EditorHandlerIllustration"
            text="Editor Add Caret"
            description="Adds a second caret below the existing one."
            icon="SdkIcons.Sdk_default_icon">
      <add-to-group group-id="EditorPopupMenu" anchor="first"/>
    </action>
    <!-- Place this entry first in the popup menu; it's always enabled if a project and editor are open -->
    <action id="EditorBasics.LogicalPositionIllustration"
            class="org.intellij.sdk.editor.EditorAreaIllustration"
            text="Caret Position"
            description="Reports information about the caret position."
            icon="SdkIcons.Sdk_default_icon">
      <keyboard-shortcut keymap="$default" first-keystroke="control alt G"/>
      <add-to-group group-id="EditorPopupMenu" anchor="first"/>
    </action>
  </actions>

  <extensions defaultExtensionNs="com.intellij">
    <typedHandler implementation="org.intellij.sdk.editor.MyTypedHandler"/>
  </extensions>

</idea-plugin>

```

# editor_basics/src/main/java/org/intellij/sdk/editor/EditorAreaIllustration.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.editor;

import com.intellij.openapi.actionSystem.ActionUpdateThread;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.editor.*;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.Messages;
import org.jetbrains.annotations.NotNull;

/**
 * If conditions support it, makes a menu visible to display information about the caret.
 */
public class EditorAreaIllustration extends AnAction {

  @Override
  public @NotNull ActionUpdateThread getActionUpdateThread() {
    return ActionUpdateThread.BGT;
  }

  /**
   * Displays a message with information about the current caret.
   *
   * @param e Event related to this action
   */
  @Override
  public void actionPerformed(@NotNull final AnActionEvent e) {
    // Get access to the editor and caret model. update() validated editor's existence.
    final Editor editor = e.getRequiredData(CommonDataKeys.EDITOR);
    final CaretModel caretModel = editor.getCaretModel();
    // Getting the primary caret ensures we get the correct one of a possible many.
    final Caret primaryCaret = caretModel.getPrimaryCaret();
    // Get the caret information
    LogicalPosition logicalPos = primaryCaret.getLogicalPosition();
    VisualPosition visualPos = primaryCaret.getVisualPosition();
    int caretOffset = primaryCaret.getOffset();
    // Build and display the caret report.
    String report = logicalPos + "\n" + visualPos + "\n" +
        "Offset: " + caretOffset;
    Messages.showInfoMessage(report, "Caret Parameters Inside The Editor");
  }

  /**
   * Sets visibility and enables this action menu item if:
   * <ul>
   *   <li>a project is open</li>
   *   <li>an editor is active</li>
   * </ul>
   *
   * @param e Event related to this action
   */
  @Override
  public void update(@NotNull final AnActionEvent e) {
    // Get required data keys
    final Project project = e.getProject();
    final Editor editor = e.getData(CommonDataKeys.EDITOR);
    // Set visibility only in case of existing project and editor
    e.getPresentation().setEnabledAndVisible(project != null && editor != null);
  }

}

```

# editor_basics/src/main/java/org/intellij/sdk/editor/MyTypedHandler.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.editor;

import com.intellij.codeInsight.editorActions.TypedHandlerDelegate;
import com.intellij.openapi.command.WriteCommandAction;
import com.intellij.openapi.editor.Document;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiFile;
import org.jetbrains.annotations.NotNull;

/**
 * This is a custom {@link TypedHandlerDelegate} that handles actions activated keystrokes in the editor.
 * The execute method inserts a fixed string at Offset 0 of the document.
 * Document changes are made in the context of a write action.
 */
final class MyTypedHandler extends TypedHandlerDelegate {

  @NotNull
  @Override
  public Result charTyped(char c, @NotNull Project project, @NotNull Editor editor, @NotNull PsiFile file) {
    // Get the document and project
    final Document document = editor.getDocument();
    // Construct the runnable to substitute the string at offset 0 in the document
    Runnable runnable = () -> document.insertString(0, "editor_basics\n");
    // Make the document change in the context of a write action.
    WriteCommandAction.runWriteCommandAction(project, runnable);
    return Result.STOP;
  }

}

```

# editor_basics/src/main/java/org/intellij/sdk/editor/EditorIllustrationAction.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.editor;

import com.intellij.openapi.actionSystem.ActionUpdateThread;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.command.WriteCommandAction;
import com.intellij.openapi.editor.Caret;
import com.intellij.openapi.editor.Document;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

/**
 * Menu action to replace a selection of characters with a fixed string.
 */
public class EditorIllustrationAction extends AnAction {

  @Override
  public @NotNull ActionUpdateThread getActionUpdateThread() {
    return ActionUpdateThread.BGT;
  }

  /**
   * Replaces the run of text selected by the primary caret with a fixed string.
   *
   * @param e Event related to this action
   */
  @Override
  public void actionPerformed(@NotNull final AnActionEvent e) {
    // Get all the required data from data keys
    // Editor and Project were verified in update(), so they are not null.
    final Editor editor = e.getRequiredData(CommonDataKeys.EDITOR);
    final Project project = e.getRequiredData(CommonDataKeys.PROJECT);
    final Document document = editor.getDocument();
    // Work off of the primary caret to get the selection info
    Caret primaryCaret = editor.getCaretModel().getPrimaryCaret();
    int start = primaryCaret.getSelectionStart();
    int end = primaryCaret.getSelectionEnd();
    // Replace the selection with a fixed string.
    // Must do this document change in a write action context.
    WriteCommandAction.runWriteCommandAction(project, () ->
        document.replaceString(start, end, "Replacement")
    );
    // De-select the text range that was just replaced
    primaryCaret.removeSelection();
  }

  /**
   * Sets visibility and enables this action menu item if:
   * <ul>
   *   <li>a project is open</li>
   *   <li>an editor is active</li>
   *   <li>some characters are selected</li>
   * </ul>
   *
   * @param e Event related to this action
   */
  @Override
  public void update(@NotNull final AnActionEvent e) {
    // Get required data keys
    final Project project = e.getProject();
    final Editor editor = e.getData(CommonDataKeys.EDITOR);
    // Set visibility and enable only in case of existing project and editor and if a selection exists
    e.getPresentation().setEnabledAndVisible(
        project != null && editor != null && editor.getSelectionModel().hasSelection()
    );
  }

}

```

# editor_basics/src/main/java/org/intellij/sdk/editor/EditorHandlerIllustration.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.editor;

import com.intellij.openapi.actionSystem.*;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.editor.actionSystem.EditorActionHandler;
import com.intellij.openapi.editor.actionSystem.EditorActionManager;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

/**
 * Menu action to clone a new caret based on an existing one.
 */
public class EditorHandlerIllustration extends AnAction {

  @Override
  public @NotNull ActionUpdateThread getActionUpdateThread() {
    return ActionUpdateThread.BGT;
  }

  /**
   * Clones a new caret at a higher Logical Position line number.
   *
   * @param e Event related to this action
   */
  @Override
  public void actionPerformed(@NotNull final AnActionEvent e) {
    // Editor is known to exist from update, so it's not null
    final Editor editor = e.getRequiredData(CommonDataKeys.EDITOR);
    // Get the action manager in order to get the necessary action handler...
    final EditorActionManager actionManager = EditorActionManager.getInstance();
    // Get the action handler registered to clone carets
    final EditorActionHandler actionHandler =
        actionManager.getActionHandler(IdeActions.ACTION_EDITOR_CLONE_CARET_BELOW);
    // Clone one caret below the active caret
    actionHandler.execute(editor, editor.getCaretModel().getPrimaryCaret(), e.getDataContext());
  }

  /**
   * Enables and sets visibility of this action menu item if:
   * <ul>
   *   <li>a project is open</li>
   *   <li>an editor is active</li>
   *   <li>at least one caret exists</li>
   * </ul>
   *
   * @param e Event related to this action
   */
  @Override
  public void update(@NotNull final AnActionEvent e) {
    final Project project = e.getProject();
    final Editor editor = e.getData(CommonDataKeys.EDITOR);
    // Make sure at least one caret is available
    boolean menuAllowed = false;
    if (editor != null && project != null) {
      // Ensure the list of carets in the editor is not empty
      menuAllowed = !editor.getCaretModel().getAllCarets().isEmpty();
    }
    e.getPresentation().setEnabledAndVisible(menuAllowed);
  }

}

```

# editor_basics/src/main/java/icons/SdkIcons.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package icons;

import com.intellij.openapi.util.IconLoader;

import javax.swing.*;

public class SdkIcons {

  public static final Icon Sdk_default_icon = IconLoader.getIcon("/icons/sdk_16.svg", SdkIcons.class);

}

```

# live_templates/README.md
# Live Templates Sample [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Live Templates in IntelliJ SDK Docs][docs:live_templates]*

## Quickstart

Live Templates Sample Project implements two example live templates for the Markdown language:

- New link reference - by typing the `{<TAB>`, the following template will be inserted: `[$TEXT$]($LINK$)$END$`
- Convert to title case - retrieves the text from the macro or selection, if available.

### Extension Points

| Name                                | Implementation                          | Extension Point Class |
|-------------------------------------|-----------------------------------------|-----------------------|
| `com.intellij.defaultLiveTemplates` | [Markdown][file:Markdown]               | n/a                   |
| `com.intellij.liveTemplateContext`  | [MarkdownContext][file:MarkdownContext] | `TemplateContextType` |
| `com.intellij.liveTemplateMacro`    | [TitleCaseMacro][file:TitleCaseMacro]   | `MacroBase`           |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:live_templates]: https://plugins.jetbrains.com/docs/intellij/live-templates.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:Markdown]: ./src/main/resources/liveTemplates/Markdown.xml
[file:MarkdownContext]: ./src/main/java/org/intellij/sdk/liveTemplates/MarkdownContext.java
[file:TitleCaseMacro]: ./src/main/java/org/intellij/sdk/liveTemplates/TitleCaseMacro.java



# live_templates/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# live_templates/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "live_templates"

```

# live_templates/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# live_templates/src/main/resources/liveTemplates/Markdown.xml
```xml
<templateSet group="Markdown">
  <template name="{"
            value="[$TEXT$]($LINK$)$END$"
            toReformat="false"
            toShortenFQNames="false"
            key="live.template.{.description" resource-bundle="messages.LiveTemplates">
    <variable name="TEXT" expression="" defaultValue="" alwaysStopAt="true"/>
    <variable name="LINK" expression="complete()" defaultValue="" alwaysStopAt="true"/>
    <context>
      <option name="MARKDOWN" value="true"/>
    </context>
  </template>
  <template name="mc"
            value="$TITLE$"
            toReformat="true"
            toShortenFQNames="false"
            key="live.template.mc.description" resource-bundle="messages.LiveTemplates">
    <variable name="TITLE" expression="titleCase(SELECTION)" defaultValue="the quick brown fox" alwaysStopAt="true" />
    <context>
      <option name="MARKDOWN" value="true" />
    </context>
  </template>
</templateSet>

```

# live_templates/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.liveTemplates</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Live Templates Sample</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.lang</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates implementing live templates for Markdown language.<br> Adds an entry to the
      <b>Settings | Editor | Live Templates</b> dialog.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.1.0</b> Use com.intellij.defaultLiveTemplates, add custom macro.</li>
        <li><b>2.0.0</b> Convert to Gradle-based plugin, change plugin ID</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <resource-bundle>messages.LiveTemplates</resource-bundle>

  <extensions defaultExtensionNs="com.intellij">
    <defaultLiveTemplates file="/liveTemplates/Markdown.xml"/>
    <liveTemplateContext implementation="org.intellij.sdk.liveTemplates.MarkdownContext"
                         contextId="MARKDOWN"/>
    <liveTemplateMacro implementation="org.intellij.sdk.liveTemplates.TitleCaseMacro"/>
  </extensions>

</idea-plugin>

```

# live_templates/src/main/java/org/intellij/sdk/liveTemplates/TitleCaseMacro.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.liveTemplates;

import com.intellij.codeInsight.template.*;
import com.intellij.codeInsight.template.macro.MacroBase;
import com.intellij.openapi.util.text.StringUtil;
import org.jetbrains.annotations.NotNull;

final class TitleCaseMacro extends MacroBase {

  public TitleCaseMacro() {
    super("titleCase", "titleCase(String)");
  }

  /**
   * Strictly to uphold contract for constructors in base class.
   */
  private TitleCaseMacro(String name, String description) {
    super(name, description);
  }

  @Override
  protected Result calculateResult(Expression @NotNull [] params, ExpressionContext context, boolean quick) {
    // Retrieve the text from the macro or selection, if any is available.
    String text = getTextResult(params, context, true);
    if (text == null) {
      return null;
    }
    if (!text.isEmpty()) {
      // Capitalize the start of every word
      text = StringUtil.toTitleCase(text);
    }
    return new TextResult(text);
  }

  @Override
  public boolean isAcceptableInContext(TemplateContextType context) {
    // Might want to be less restrictive in future
    return (context instanceof MarkdownContext);
  }

}

```

# live_templates/src/main/java/org/intellij/sdk/liveTemplates/MarkdownContext.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.liveTemplates;

import com.intellij.codeInsight.template.TemplateActionContext;
import com.intellij.codeInsight.template.TemplateContextType;
import org.jetbrains.annotations.NotNull;

final class MarkdownContext extends TemplateContextType {

  MarkdownContext() {
    super("Markdown");
  }

  @Override
  public boolean isInContext(@NotNull TemplateActionContext templateActionContext) {
    return templateActionContext.getFile().getName().endsWith(".md");
  }

}

```

# tree_structure_provider/README.md
# Tree Structure Provider Sample [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Tree Structure View in IntelliJ SDK Docs][docs:tree_structure_view]*

## Quickstart

The Tree Structure Provider sample project implements `com.intellij.treeStructureProvider` Extension Point, which allows modifying the structure of the project tree in the _Project View_ panel.
This implementation limits the presented files to the Plain Text files only.

The current implementation checks if a Project View node represents a directory or file of the `PlainTextFileType` type.
Otherwise, an element is not included in the results list, so only directories and plain text files are rendered.

### Extension Points

| Name                                 | Implementation                                                      | Extension Point Class   |
|--------------------------------------|---------------------------------------------------------------------|-------------------------|
| `com.intellij.treeStructureProvider` | [TextOnlyTreeStructureProvider][file:TextOnlyTreeStructureProvider] | `TreeStructureProvider` |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:tree_structure_view]: https://plugins.jetbrains.com/docs/intellij/tree-structure-view.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:TextOnlyTreeStructureProvider]: ./src/main/java/org/intellij/sdk/treeStructureProvider/TextOnlyTreeStructureProvider.java


# tree_structure_provider/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# tree_structure_provider/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "tree_structure_provider"

```

# tree_structure_provider/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# tree_structure_provider/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.treeStructureProvider</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Tree Structure Provider Sample</name>

  <!-- Indicate this plugin can be loaded in all IntelliJ Platform-based products. -->
  <depends>com.intellij.modules.platform</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Tree Structure Provider showing only plain text files.
      <br>See the <a href="https://plugins.jetbrains.com/docs/intellij/tree-structure-view.html">Tree
      Structure View</a> for more information.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin.</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <treeStructureProvider implementation="org.intellij.sdk.treeStructureProvider.TextOnlyTreeStructureProvider"/>
  </extensions>

</idea-plugin>

```

# tree_structure_provider/src/main/java/org/intellij/sdk/treeStructureProvider/TextOnlyTreeStructureProvider.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.treeStructureProvider;

import com.intellij.ide.projectView.TreeStructureProvider;
import com.intellij.ide.projectView.ViewSettings;
import com.intellij.ide.projectView.impl.nodes.PsiFileNode;
import com.intellij.ide.util.treeView.AbstractTreeNode;
import com.intellij.openapi.fileTypes.PlainTextFileType;
import com.intellij.openapi.vfs.VirtualFile;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.Collection;

final class TextOnlyTreeStructureProvider implements TreeStructureProvider {

  @NotNull
  @Override
  public Collection<AbstractTreeNode<?>> modify(@NotNull AbstractTreeNode<?> parent,
                                                @NotNull Collection<AbstractTreeNode<?>> children,
                                                ViewSettings settings) {
    ArrayList<AbstractTreeNode<?>> nodes = new ArrayList<>();
    for (AbstractTreeNode<?> child : children) {
      if (child instanceof PsiFileNode) {
        VirtualFile file = ((PsiFileNode) child).getVirtualFile();
        if (file != null && !file.isDirectory() && !(file.getFileType() instanceof PlainTextFileType)) {
          continue;
        }
      }
      nodes.add(child);
    }
    return nodes;
  }

}

```

# CONTRIBUTING.md
<!-- Copyright 2000-2024 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->

Before you begin contributing content to the SDK, please read this page thoroughly as well as the [Code of Conduct](/CODE_OF_CONDUCT.md) and [License](/LICENSE.txt) documents.

> [!IMPORTANT]
> This [intellij-sdk-code-samples](https://github.com/JetBrains/intellij-sdk-code-samples) is a mirror of the [IntelliJ SDK Docs Code Samples](https://github.com/JetBrains/intellij-sdk-docs/tree/main/code_samples).
> Any pull requests should be performed on the [IntelliJ SDK Docs](https://github.com/JetBrains/intellij-sdk-docs) repository.

For more details regarding the Code Samples contribution, please read the [Guidelines for Creating IntelliJ Platform SDK Code Samples](https://plugins.jetbrains.com/docs/intellij/sdk-code-guidelines.html).


# simple_language_plugin/README.md
# Simple Language Sample [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Custom Language Support Tutorial in IntelliJ SDK Docs][docs:custom_language_support_tutorial]*

## Quickstart

Defines a new language, _Simple language_ with support for syntax highlighting, annotations, code completion, and other features.

### Extension Points

| Name                                          | Implementation                                                                          | Extension Point Class               |
|-----------------------------------------------|-----------------------------------------------------------------------------------------|-------------------------------------|
| `com.intellij.fileType`                       | [SimpleFileType][file:SimpleFileType]                                                   | `LanguageFileType`                  |
| `com.intellij.lang.parserDefinition`          | [SimpleParserDefinition][file:SimpleParserDefinition]                                   | `ParserDefinition`                  |
| `com.intellij.lang.syntaxHighlighterFactory`  | [SimpleSyntaxHighlighterFactory][file:SimpleSyntaxHighlighterFactory]                   | `SyntaxHighlighterFactory`          |
| `com.intellij.colorSettingsPage`              | [SimpleColorSettingsPage][file:SimpleColorSettingsPage]                                 | `ColorSettingsPage`                 |
| `com.intellij.annotator`                      | [SimpleAnnotator][file:SimpleAnnotator]                                                 | `Annotator`                         |
| `com.intellij.codeInsight.lineMarkerProvider` | [SimpleLineMarkerProvider][file:SimpleLineMarkerProvider]                               | `RelatedItemLineMarkerProvider`     |
| `com.intellij.completion.contributor`         | [SimpleCompletionContributor][file:SimpleCompletionContributor]                         | `CompletionContributor`             |
| `com.intellij.psi.referenceContributor`       | [SimpleReferenceContributor][file:SimpleReferenceContributor]                           | `PsiReferenceContributor`           |
| `com.intellij.lang.refactoringSupport`        | [SimpleRefactoringSupportProvider][file:SimpleRefactoringSupportProvider]               | `RefactoringSupportProvider`        |
| `com.intellij.lang.findUsagesProvider`        | [SimpleFindUsagesProvider][file:SimpleFindUsagesProvider]                               | `FindUsagesProvider`                |
| `com.intellij.lang.foldingBuilder`            | [SimpleFoldingBuilder][file:SimpleFoldingBuilder]                                       | `FoldingBuilderEx`                  |
| `com.intellij.gotoSymbolContributor`          | [SimpleChooseByNameContributor][file:SimpleChooseByNameContributor]                     | `ChooseByNameContributor`           |
| `com.intellij.lang.psiStructureViewFactory`   | [SimpleStructureViewFactory][file:SimpleStructureViewFactory]                           | `PsiStructureViewFactory`           |
| `com.intellij.lang.formatter`                 | [SimpleFormattingModelBuilder][file:SimpleFormattingModelBuilder]                       | `FormattingModelBuilder`            |
| `com.intellij.codeStyleSettingsProvider`      | [SimpleCodeStyleSettingsProvider][file:SimpleCodeStyleSettingsProvider]                 | `CodeStyleSettingsProvider`         |
| `com.intellij.langCodeStyleSettingsProvider`  | [SimpleLanguageCodeStyleSettingsProvider][file:SimpleLanguageCodeStyleSettingsProvider] | `LanguageCodeStyleSettingsProvider` |
| `com.intellij.lang.commenter`                 | [SimpleCommenter][file:SimpleCommenter]                                                 | `Commenter`                         |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:custom_language_support_tutorial]: https://plugins.jetbrains.com/docs/intellij/custom-language-support-tutorial.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:SimpleFileType]: ./src/main/java/org/intellij/sdk/language/SimpleFileType.java
[file:SimpleParserDefinition]: ./src/main/java/org/intellij/sdk/language/SimpleParserDefinition.java
[file:SimpleSyntaxHighlighterFactory]: ./src/main/java/org/intellij/sdk/language/SimpleSyntaxHighlighterFactory.java
[file:SimpleColorSettingsPage]: ./src/main/java/org/intellij/sdk/language/SimpleColorSettingsPage.java
[file:SimpleAnnotator]: ./src/main/java/org/intellij/sdk/language/SimpleAnnotator.java
[file:SimpleLineMarkerProvider]: ./src/main/java/org/intellij/sdk/language/SimpleLineMarkerProvider.java
[file:SimpleCompletionContributor]: ./src/main/java/org/intellij/sdk/language/SimpleCompletionContributor.java
[file:SimpleReferenceContributor]: ./src/main/java/org/intellij/sdk/language/SimpleReferenceContributor.java
[file:SimpleRefactoringSupportProvider]: ./src/main/java/org/intellij/sdk/language/SimpleRefactoringSupportProvider.java
[file:SimpleFindUsagesProvider]: ./src/main/java/org/intellij/sdk/language/SimpleFindUsagesProvider.java
[file:SimpleFoldingBuilder]: ./src/main/java/org/intellij/sdk/language/SimpleFoldingBuilder.java
[file:SimpleChooseByNameContributor]: ./src/main/java/org/intellij/sdk/language/SimpleChooseByNameContributor.java
[file:SimpleStructureViewFactory]: ./src/main/java/org/intellij/sdk/language/SimpleStructureViewFactory.java
[file:SimpleFormattingModelBuilder]: ./src/main/java/org/intellij/sdk/language/SimpleFormattingModelBuilder.java
[file:SimpleCodeStyleSettingsProvider]: ./src/main/java/org/intellij/sdk/language/SimpleCodeStyleSettingsProvider.java
[file:SimpleLanguageCodeStyleSettingsProvider]: ./src/main/java/org/intellij/sdk/language/SimpleLanguageCodeStyleSettingsProvider.java
[file:SimpleCommenter]: ./src/main/java/org/intellij/sdk/language/SimpleCommenter.java



# simple_language_plugin/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

// Include the generated files in the source set
sourceSets {
  main {
    java {
      srcDirs("src/main/gen")
    }
  }
}

dependencies {
  testImplementation("junit:junit:4.13.2")
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
  plugins.set(listOf("com.intellij.java"))
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# simple_language_plugin/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "simple_language_plugin"

```

# simple_language_plugin/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# simple_language_plugin/src/test/testData/AnnotatorTestData.java
```java
public class Test {
  public static void main(String[] args) {
    System.out.println("simple:website");
    System.out.println("simple:key with spaces");
    System.out.println("simple:<error descr="Unresolved property">websit</error>");
  }
}

```

# simple_language_plugin/src/test/testData/FindUsagesTestData.java
```java
public class Test {
  public static void main(String[] args) {
    System.out.println("simple:key with spaces");
  }
}

```

# simple_language_plugin/src/test/testData/DocumentationTestData.java
```java
public class Test {
  public static void main(String[] args) {
    System.out.println("simple:website<caret>");
  }
}

```

# simple_language_plugin/src/test/testData/CompleteTestData.java
```java
public class Test {
  public static void main(String[] args) {
    System.out.println("simple:<caret>");
  }
}

```

# simple_language_plugin/src/test/testData/FoldingTestData.java
```java
public class Test {
    public static void main(String[] args)<fold text=' { '> {
        </fold>System.out.println("<fold text='https://en.wikipedia.org/'>simple:website</fold>");<fold text=' }'>
    }</fold>
    public static void main1(String[] args)<fold text=' { '> {
        </fold>System.out.println("<fold text='This is the value that could be looked up with the key \"key with spaces\".'>simple:key with spaces</fold>");<fold text=' }'>
    }</fold>
    public static void main2(String[] args)<fold text=' { '> {
        </fold>System.out.println("<fold text='Welcome to \n          Wikipedia!'>simple:message</fold>");<fold text=' }'>
    }</fold>
}

```

# simple_language_plugin/src/test/testData/RenameTestData.java
```java
public class Test {
  public static void main(String[] args) {
    System.out.println("simple:website<caret>");
  }
}

```

# simple_language_plugin/src/test/testData/ReferenceTestData.java
```java
public class Test {
  public static void main(String[] args) {
    System.out.println("simple:website<caret>");
  }
}

```

# simple_language_plugin/src/test/java/org/intellij/sdk/language/SimpleParsingTest.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.testFramework.ParsingTestCase;

public class SimpleParsingTest extends ParsingTestCase {

  public SimpleParsingTest() {
    super("", "simple", new SimpleParserDefinition());
  }

  public void testParsingTestData() {
    doTest(true);
  }

  /**
   * @return path to test data file directory relative to root of this module.
   */
  @Override
  protected String getTestDataPath() {
    return "src/test/testData";
  }

  @Override
  protected boolean includeRanges() {
    return true;
  }

}

```

# simple_language_plugin/src/test/java/org/intellij/sdk/language/SimpleCodeInsightTest.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.application.options.CodeStyle;
import com.intellij.codeInsight.completion.CompletionType;
import com.intellij.codeInsight.documentation.DocumentationManager;
import com.intellij.codeInsight.generation.actions.CommentByLineCommentAction;
import com.intellij.lang.documentation.DocumentationProvider;
import com.intellij.openapi.command.WriteCommandAction;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiReference;
import com.intellij.psi.codeStyle.CodeStyleManager;
import com.intellij.testFramework.fixtures.LightJavaCodeInsightFixtureTestCase;
import com.intellij.usageView.UsageInfo;
import org.intellij.sdk.language.psi.SimpleProperty;

import java.util.Collection;
import java.util.List;

public class SimpleCodeInsightTest extends LightJavaCodeInsightFixtureTestCase {

  /**
   * @return path to test data file directory relative to working directory in the run configuration for this test.
   */
  @Override
  protected String getTestDataPath() {
    return "src/test/testData";
  }

  public void testCompletion() {
    myFixture.configureByFiles("CompleteTestData.java", "DefaultTestData.simple");
    myFixture.complete(CompletionType.BASIC);
    List<String> lookupElementStrings = myFixture.getLookupElementStrings();
    assertNotNull(lookupElementStrings);
    assertSameElements(lookupElementStrings, "key with spaces", "language", "message", "tab", "website");
  }

  public void testAnnotator() {
    myFixture.configureByFiles("AnnotatorTestData.java", "DefaultTestData.simple");
    myFixture.checkHighlighting(false, false, false, true);
  }

  public void testFormatter() {
    myFixture.configureByFile("FormatterTestData.simple");
    CodeStyle.getLanguageSettings(myFixture.getFile()).SPACE_AROUND_ASSIGNMENT_OPERATORS = true;
    CodeStyle.getLanguageSettings(myFixture.getFile()).KEEP_BLANK_LINES_IN_CODE = 2;
    WriteCommandAction.writeCommandAction(getProject()).run(() ->
        CodeStyleManager.getInstance(getProject()).reformatText(
            myFixture.getFile(),
            List.of(myFixture.getFile().getTextRange())
        )
    );
    myFixture.checkResultByFile("DefaultTestData.simple");
  }

  public void testRename() {
    myFixture.configureByFiles("RenameTestData.java", "RenameTestData.simple");
    myFixture.renameElementAtCaret("websiteUrl");
    myFixture.checkResultByFile("RenameTestData.simple", "RenameTestDataAfter.simple", false);
  }

  public void testFolding() {
    myFixture.configureByFile("DefaultTestData.simple");
    myFixture.testFolding(getTestDataPath() + "/FoldingTestData.java");
  }

  public void testFindUsages() {
    Collection<UsageInfo> usageInfos = myFixture.testFindUsages("FindUsagesTestData.simple", "FindUsagesTestData.java");
    assertEquals(1, usageInfos.size());
  }

  public void testCommenter() {
    myFixture.configureByText(SimpleFileType.INSTANCE, "<caret>website = https://en.wikipedia.org/");
    CommentByLineCommentAction commentAction = new CommentByLineCommentAction();
    commentAction.actionPerformedImpl(getProject(), myFixture.getEditor());
    myFixture.checkResult("#website = https://en.wikipedia.org/");
    commentAction.actionPerformedImpl(getProject(), myFixture.getEditor());
    myFixture.checkResult("website = https://en.wikipedia.org/");
  }

  public void testReference() {
    PsiReference referenceAtCaret =
        myFixture.getReferenceAtCaretPositionWithAssertion("ReferenceTestData.java", "DefaultTestData.simple");
    final SimpleProperty resolvedSimpleProperty = assertInstanceOf(referenceAtCaret.resolve(), SimpleProperty.class);
    assertEquals("https://en.wikipedia.org/", resolvedSimpleProperty.getValue());
  }

  public void testDocumentation() {
    myFixture.configureByFiles("DocumentationTestData.java", "DocumentationTestData.simple");
    final PsiElement originalElement = myFixture.getElementAtCaret();
    PsiElement element = DocumentationManager
        .getInstance(getProject())
        .findTargetElement(myFixture.getEditor(), originalElement.getContainingFile(), originalElement);

    if (element == null) {
      element = originalElement;
    }

    final DocumentationProvider documentationProvider = DocumentationManager.getProviderFromElement(element);
    final String generateDoc = documentationProvider.generateDoc(element, originalElement);
    assertNotNull(generateDoc);
    assertSameLinesWithFile(getTestDataPath() + "/" + "DocumentationTest.html.expected", generateDoc);
  }

}

```

# simple_language_plugin/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.language</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Simple Language Sample</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.platform</depends>
  <depends>com.intellij.java</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates how to add custom language support to an IntelliJ Platform-based IDE. <br>Defines a new language,
      <i>Simple language</i> with support for syntax highlighting, annotations, code completion, and other features.
      <br>
      See the
      <a href="https://plugins.jetbrains.com/docs/intellij/custom-language-support-tutorial.html">Custom
      Language Tutorial</a> for more information.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin.</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <fileType name="Simple File" implementationClass="org.intellij.sdk.language.SimpleFileType" fieldName="INSTANCE"
              language="Simple" extensions="simple"/>
    <lang.parserDefinition language="Simple" implementationClass="org.intellij.sdk.language.SimpleParserDefinition"/>
    <lang.syntaxHighlighterFactory language="Simple"
                                   implementationClass="org.intellij.sdk.language.SimpleSyntaxHighlighterFactory"/>
    <iconProvider implementation="org.intellij.sdk.language.SimplePropertyIconProvider"/>
    <colorSettingsPage implementation="org.intellij.sdk.language.SimpleColorSettingsPage"/>
    <annotator language="JAVA" implementationClass="org.intellij.sdk.language.SimpleAnnotator"/>
    <codeInsight.lineMarkerProvider language="JAVA"
                                    implementationClass="org.intellij.sdk.language.SimpleLineMarkerProvider"/>
    <completion.contributor language="Simple"
                            implementationClass="org.intellij.sdk.language.SimpleCompletionContributor"/>
    <psi.referenceContributor language="JAVA"
                              implementation="org.intellij.sdk.language.SimpleReferenceContributor"/>
    <lang.refactoringSupport language="Simple"
                             implementationClass="org.intellij.sdk.language.SimpleRefactoringSupportProvider"/>
    <lang.findUsagesProvider language="Simple"
                             implementationClass="org.intellij.sdk.language.SimpleFindUsagesProvider"/>
    <lang.foldingBuilder language="JAVA" implementationClass="org.intellij.sdk.language.SimpleFoldingBuilder"/>
    <gotoSymbolContributor implementation="org.intellij.sdk.language.SimpleChooseByNameContributor"/>
    <lang.psiStructureViewFactory language="Simple"
                                  implementationClass="org.intellij.sdk.language.SimpleStructureViewFactory"/>
    <navbar implementation="org.intellij.sdk.language.SimpleStructureAwareNavbar"/>
    <lang.formatter language="Simple" implementationClass="org.intellij.sdk.language.SimpleFormattingModelBuilder"/>
    <codeStyleSettingsProvider implementation="org.intellij.sdk.language.SimpleCodeStyleSettingsProvider"/>
    <langCodeStyleSettingsProvider implementation="org.intellij.sdk.language.SimpleLanguageCodeStyleSettingsProvider"/>
    <lang.commenter language="Simple" implementationClass="org.intellij.sdk.language.SimpleCommenter"/>
    <lang.documentationProvider language="Simple" implementationClass="org.intellij.sdk.language.SimpleDocumentationProvider"/>
    <spellchecker.support language="Simple" implementationClass="org.intellij.sdk.language.SimpleSpellcheckingStrategy"/>
  </extensions>

</idea-plugin>

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleCommenter.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.lang.Commenter;
import org.jetbrains.annotations.Nullable;

final class SimpleCommenter implements Commenter {

  @Override
  public String getLineCommentPrefix() {
    return "#";
  }

  @Override
  public String getBlockCommentPrefix() {
    return "";
  }

  @Nullable
  @Override
  public String getBlockCommentSuffix() {
    return null;
  }

  @Nullable
  @Override
  public String getCommentedBlockCommentPrefix() {
    return null;
  }

  @Nullable
  @Override
  public String getCommentedBlockCommentSuffix() {
    return null;
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleSpellcheckingStrategy.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.lang.ASTNode;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiComment;
import com.intellij.psi.PsiElement;
import com.intellij.spellchecker.inspections.CommentSplitter;
import com.intellij.spellchecker.inspections.IdentifierSplitter;
import com.intellij.spellchecker.inspections.PlainTextSplitter;
import com.intellij.spellchecker.tokenizer.SpellcheckingStrategy;
import com.intellij.spellchecker.tokenizer.TokenConsumer;
import com.intellij.spellchecker.tokenizer.Tokenizer;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.intellij.sdk.language.psi.SimpleTypes;
import org.jetbrains.annotations.NotNull;

final class SimpleSpellcheckingStrategy extends SpellcheckingStrategy {

  @Override
  public @NotNull Tokenizer<?> getTokenizer(PsiElement element) {
    if (element instanceof PsiComment) {
      return new SimpleCommentTokenizer();
    }

    if (element instanceof SimpleProperty) {
      return new SimplePropertyTokenizer();
    }

    return EMPTY_TOKENIZER;
  }

  private static class SimpleCommentTokenizer extends Tokenizer<PsiComment> {

    @Override
    public void tokenize(@NotNull PsiComment element, @NotNull TokenConsumer consumer) {
      // Exclude the start of the comment with its # characters from spell checking
      int startIndex = 0;
      for (char c : element.textToCharArray()) {
        if (c == '#' || Character.isWhitespace(c)) {
          startIndex++;
        } else {
          break;
        }
      }
      consumer.consumeToken(element, element.getText(), false, 0,
          TextRange.create(startIndex, element.getTextLength()),
          CommentSplitter.getInstance());
    }

  }

  private static class SimplePropertyTokenizer extends Tokenizer<SimpleProperty> {

    public void tokenize(@NotNull SimpleProperty element, @NotNull TokenConsumer consumer) {
      //Spell check the keys and values of properties with different splitters
      final ASTNode key = element.getNode().findChildByType(SimpleTypes.KEY);
      if (key != null && key.getTextLength() > 0) {
        final PsiElement keyPsi = key.getPsi();
        final String text = key.getText();
        //For keys, use a splitter for identifiers
        //Note we set "useRename" to true so that keys will be properly refactored (renamed)
        consumer.consumeToken(keyPsi, text, true, 0,
            TextRange.allOf(text), IdentifierSplitter.getInstance());
      }

      final ASTNode value = element.getNode().findChildByType(SimpleTypes.VALUE);
      if (value != null && value.getTextLength() > 0) {
        final PsiElement valuePsi = value.getPsi();
        final String text = valuePsi.getText();
        //For values, use a splitter for plain text
        consumer.consumeToken(valuePsi, text, false, 0,
            TextRange.allOf(text), PlainTextSplitter.getInstance());
      }
    }

  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleFindUsagesProvider.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.lang.cacheBuilder.DefaultWordsScanner;
import com.intellij.lang.cacheBuilder.WordsScanner;
import com.intellij.lang.findUsages.FindUsagesProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiNamedElement;
import com.intellij.psi.tree.TokenSet;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.intellij.sdk.language.psi.SimpleTokenSets;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

final class SimpleFindUsagesProvider implements FindUsagesProvider {

  @Override
  public WordsScanner getWordsScanner() {
    return new DefaultWordsScanner(new SimpleLexerAdapter(),
        SimpleTokenSets.IDENTIFIERS,
        SimpleTokenSets.COMMENTS,
        TokenSet.EMPTY);
  }

  @Override
  public boolean canFindUsagesFor(@NotNull PsiElement psiElement) {
    return psiElement instanceof PsiNamedElement;
  }

  @Nullable
  @Override
  public String getHelpId(@NotNull PsiElement psiElement) {
    return null;
  }

  @NotNull
  @Override
  public String getType(@NotNull PsiElement element) {
    if (element instanceof SimpleProperty) {
      return "simple property";
    }
    return "";
  }

  @NotNull
  @Override
  public String getDescriptiveName(@NotNull PsiElement element) {
    if (element instanceof SimpleProperty) {
      return ((SimpleProperty) element).getKey();
    }
    return "";
  }

  @NotNull
  @Override
  public String getNodeText(@NotNull PsiElement element, boolean useFullName) {
    if (element instanceof SimpleProperty) {
      return ((SimpleProperty) element).getKey() +
          SimpleAnnotator.SIMPLE_SEPARATOR_STR +
          ((SimpleProperty) element).getValue();
    }
    return "";
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleLexerAdapter.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.lexer.FlexAdapter;

public class SimpleLexerAdapter extends FlexAdapter {

  public SimpleLexerAdapter() {
    super(new SimpleLexer(null));
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleStructureViewModel.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.ide.structureView.StructureViewModel;
import com.intellij.ide.structureView.StructureViewModelBase;
import com.intellij.ide.structureView.StructureViewTreeElement;
import com.intellij.ide.util.treeView.smartTree.Sorter;
import com.intellij.openapi.editor.Editor;
import com.intellij.psi.PsiFile;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class SimpleStructureViewModel extends StructureViewModelBase implements
    StructureViewModel.ElementInfoProvider {

  public SimpleStructureViewModel(@Nullable Editor editor, PsiFile psiFile) {
    super(psiFile, editor, new SimpleStructureViewElement(psiFile));
  }

  @NotNull
  public Sorter @NotNull [] getSorters() {
    return new Sorter[]{Sorter.ALPHA_SORTER};
  }


  @Override
  public boolean isAlwaysShowsPlus(StructureViewTreeElement element) {
    return false;
  }

  @Override
  public boolean isAlwaysLeaf(StructureViewTreeElement element) {
    return element.getValue() instanceof SimpleProperty;
  }

  @Override
  protected Class<?> @NotNull [] getSuitableClasses() {
    return new Class[]{SimpleProperty.class};
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleCodeStyleSettingsProvider.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.application.options.CodeStyleAbstractConfigurable;
import com.intellij.application.options.CodeStyleAbstractPanel;
import com.intellij.application.options.TabbedLanguageCodeStylePanel;
import com.intellij.psi.codeStyle.CodeStyleConfigurable;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CodeStyleSettingsProvider;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;
import org.jetbrains.annotations.NotNull;

final class SimpleCodeStyleSettingsProvider extends CodeStyleSettingsProvider {

  @Override
  public CustomCodeStyleSettings createCustomSettings(@NotNull CodeStyleSettings settings) {
    return new SimpleCodeStyleSettings(settings);
  }

  @Override
  public String getConfigurableDisplayName() {
    return "Simple";
  }

  @NotNull
  public CodeStyleConfigurable createConfigurable(@NotNull CodeStyleSettings settings,
                                                  @NotNull CodeStyleSettings modelSettings) {
    return new CodeStyleAbstractConfigurable(settings, modelSettings, this.getConfigurableDisplayName()) {
      @Override
      protected @NotNull CodeStyleAbstractPanel createPanel(@NotNull CodeStyleSettings settings) {
        return new SimpleCodeStyleMainPanel(getCurrentSettings(), settings);
      }
    };
  }

  private static class SimpleCodeStyleMainPanel extends TabbedLanguageCodeStylePanel {

    public SimpleCodeStyleMainPanel(CodeStyleSettings currentSettings, CodeStyleSettings settings) {
      super(SimpleLanguage.INSTANCE, currentSettings, settings);
    }

  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleCodeStyleSettings.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;

public class SimpleCodeStyleSettings extends CustomCodeStyleSettings {

  public SimpleCodeStyleSettings(CodeStyleSettings settings) {
    super("SimpleCodeStyleSettings", settings);
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleStructureViewFactory.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.ide.structureView.StructureViewBuilder;
import com.intellij.ide.structureView.StructureViewModel;
import com.intellij.ide.structureView.TreeBasedStructureViewBuilder;
import com.intellij.lang.PsiStructureViewFactory;
import com.intellij.openapi.editor.Editor;
import com.intellij.psi.PsiFile;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

final class SimpleStructureViewFactory implements PsiStructureViewFactory {

  @Override
  public StructureViewBuilder getStructureViewBuilder(@NotNull final PsiFile psiFile) {
    return new TreeBasedStructureViewBuilder() {
      @NotNull
      @Override
      public StructureViewModel createStructureViewModel(@Nullable Editor editor) {
        return new SimpleStructureViewModel(editor, psiFile);
      }
    };
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleCreatePropertyQuickFix.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.codeInsight.intention.impl.BaseIntentionAction;
import com.intellij.lang.ASTNode;
import com.intellij.openapi.application.ApplicationManager;
import com.intellij.openapi.command.WriteCommandAction;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.fileChooser.FileChooser;
import com.intellij.openapi.fileChooser.FileChooserDescriptor;
import com.intellij.openapi.fileChooser.FileChooserDescriptorFactory;
import com.intellij.openapi.fileEditor.FileEditorManager;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.project.ProjectUtil;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.pom.Navigatable;
import com.intellij.psi.PsiFile;
import com.intellij.psi.PsiManager;
import com.intellij.psi.search.FileTypeIndex;
import com.intellij.psi.search.GlobalSearchScope;
import com.intellij.util.IncorrectOperationException;
import org.intellij.sdk.language.psi.SimpleElementFactory;
import org.intellij.sdk.language.psi.SimpleFile;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;

import java.util.Collection;

class SimpleCreatePropertyQuickFix extends BaseIntentionAction {

  private final String key;

  SimpleCreatePropertyQuickFix(String key) {
    this.key = key;
  }

  @NotNull
  @Override
  public String getText() {
    return "Create property '" + key + "'";
  }

  @NotNull
  @Override
  public String getFamilyName() {
    return "Create property";
  }

  @Override
  public boolean isAvailable(@NotNull Project project, Editor editor, PsiFile file) {
    return true;
  }

  @Override
  public void invoke(@NotNull final Project project, final Editor editor, PsiFile file) throws
      IncorrectOperationException {
    ApplicationManager.getApplication().invokeLater(() -> {
      Collection<VirtualFile> virtualFiles =
          FileTypeIndex.getFiles(SimpleFileType.INSTANCE, GlobalSearchScope.allScope(project));
      if (virtualFiles.size() == 1) {
        createProperty(project, virtualFiles.iterator().next());
      } else {
        final FileChooserDescriptor descriptor =
            FileChooserDescriptorFactory.createSingleFileDescriptor(SimpleFileType.INSTANCE);
        descriptor.setRoots(ProjectUtil.guessProjectDir(project));
        final VirtualFile file1 = FileChooser.chooseFile(descriptor, project, null);
        if (file1 != null) {
          createProperty(project, file1);
        }
      }
    });
  }

  private void createProperty(final Project project, final VirtualFile file) {
    WriteCommandAction.writeCommandAction(project).run(() -> {
      SimpleFile simpleFile = (SimpleFile) PsiManager.getInstance(project).findFile(file);
      assert simpleFile != null;
      ASTNode lastChildNode = simpleFile.getNode().getLastChildNode();
      // TODO: Add another check for CRLF
      if (lastChildNode != null/* && !lastChildNode.getElementType().equals(SimpleTypes.CRLF)*/) {
        simpleFile.getNode().addChild(SimpleElementFactory.createCRLF(project).getNode());
      }
      // IMPORTANT: change spaces to escaped spaces or the new node will only have the first word for the key
      SimpleProperty property = SimpleElementFactory.createProperty(project, key.replaceAll(" ", "\\\\ "), "");
      simpleFile.getNode().addChild(property.getNode());
      ((Navigatable) property.getLastChild().getNavigationElement()).navigate(true);
      Editor editor = FileEditorManager.getInstance(project).getSelectedTextEditor();
      assert editor != null;
      editor.getCaretModel().moveCaretRelatively(2, 0, false, false, false);
    });
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleLineMarkerProvider.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.codeInsight.daemon.RelatedItemLineMarkerInfo;
import com.intellij.codeInsight.daemon.RelatedItemLineMarkerProvider;
import com.intellij.codeInsight.navigation.NavigationGutterIconBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiLiteralExpression;
import com.intellij.psi.impl.source.tree.java.PsiJavaTokenImpl;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;

import java.util.Collection;
import java.util.List;

final class SimpleLineMarkerProvider extends RelatedItemLineMarkerProvider {

  @Override
  protected void collectNavigationMarkers(@NotNull PsiElement element,
                                          @NotNull Collection<? super RelatedItemLineMarkerInfo<?>> result) {
    // This must be an element with a literal expression as a parent
    if (!(element instanceof PsiJavaTokenImpl) || !(element.getParent() instanceof PsiLiteralExpression literalExpression)) {
      return;
    }

    // The literal expression must start with the Simple language literal expression
    String value = literalExpression.getValue() instanceof String ? (String) literalExpression.getValue() : null;
    if ((value == null) ||
        !value.startsWith(SimpleAnnotator.SIMPLE_PREFIX_STR + SimpleAnnotator.SIMPLE_SEPARATOR_STR)) {
      return;
    }

    // Get the Simple language property usage
    Project project = element.getProject();
    String possibleProperties = value.substring(
        SimpleAnnotator.SIMPLE_PREFIX_STR.length() + SimpleAnnotator.SIMPLE_SEPARATOR_STR.length()
    );
    final List<SimpleProperty> properties = SimpleUtil.findProperties(project, possibleProperties);
    if (!properties.isEmpty()) {
      // Add the property to a collection of line marker info
      NavigationGutterIconBuilder<PsiElement> builder =
          NavigationGutterIconBuilder.create(SimpleIcons.FILE)
              .setTargets(properties)
              .setTooltipText("Navigate to Simple language property");
      result.add(builder.createLineMarkerInfo(element));
    }
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleLanguageCodeStyleSettingsProvider.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.lang.Language;
import com.intellij.psi.codeStyle.CodeStyleSettingsCustomizable;
import com.intellij.psi.codeStyle.LanguageCodeStyleSettingsProvider;
import org.jetbrains.annotations.NotNull;

final class SimpleLanguageCodeStyleSettingsProvider extends LanguageCodeStyleSettingsProvider {

  @NotNull
  @Override
  public Language getLanguage() {
    return SimpleLanguage.INSTANCE;
  }

  @Override
  public void customizeSettings(@NotNull CodeStyleSettingsCustomizable consumer, @NotNull SettingsType settingsType) {
    if (settingsType == SettingsType.SPACING_SETTINGS) {
      consumer.showStandardOptions("SPACE_AROUND_ASSIGNMENT_OPERATORS");
      consumer.renameStandardOption("SPACE_AROUND_ASSIGNMENT_OPERATORS", "Separator");
    } else if (settingsType == SettingsType.BLANK_LINES_SETTINGS) {
      consumer.showStandardOptions("KEEP_BLANK_LINES_IN_CODE");
    }
  }

  @Override
  public String getCodeSample(@NotNull SettingsType settingsType) {
    return """
        # You are reading the ".properties" entry.
        ! The exclamation mark can also mark text as comments.
        website = https://en.wikipedia.org/

        language = English
        # The backslash below tells the application to continue reading
        # the value onto the next line.
        message = Welcome to \\
                  Wikipedia!
        # Add spaces to the key
        key\\ with\\ spaces = This is the value that could be looked up with the key "key with spaces".
        # Unicode
        tab : \\u0009""";
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleFoldingBuilder.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.lang.ASTNode;
import com.intellij.lang.folding.FoldingBuilderEx;
import com.intellij.lang.folding.FoldingDescriptor;
import com.intellij.openapi.editor.Document;
import com.intellij.openapi.editor.FoldingGroup;
import com.intellij.openapi.project.DumbAware;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.openapi.util.text.StringUtil;
import com.intellij.psi.JavaRecursiveElementWalkingVisitor;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiLiteralExpression;
import com.intellij.psi.util.PsiLiteralUtil;
import com.intellij.util.containers.ContainerUtil;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

final class SimpleFoldingBuilder extends FoldingBuilderEx implements DumbAware {

  @Override
  public FoldingDescriptor @NotNull [] buildFoldRegions(@NotNull PsiElement root,
                                                        @NotNull Document document,
                                                        boolean quick) {
    // Initialize the group of folding regions that will expand/collapse together.
    FoldingGroup group = FoldingGroup.newGroup(SimpleAnnotator.SIMPLE_PREFIX_STR);
    // Initialize the list of folding regions
    List<FoldingDescriptor> descriptors = new ArrayList<>();

    root.accept(new JavaRecursiveElementWalkingVisitor() {

      @Override
      public void visitLiteralExpression(@NotNull PsiLiteralExpression literalExpression) {
        super.visitLiteralExpression(literalExpression);

        String value = PsiLiteralUtil.getStringLiteralContent(literalExpression);
        if (value != null &&
            value.startsWith(SimpleAnnotator.SIMPLE_PREFIX_STR + SimpleAnnotator.SIMPLE_SEPARATOR_STR)) {
          Project project = literalExpression.getProject();
          String key = value.substring(
              SimpleAnnotator.SIMPLE_PREFIX_STR.length() + SimpleAnnotator.SIMPLE_SEPARATOR_STR.length()
          );
          // find SimpleProperty for the given key in the project
          SimpleProperty simpleProperty = ContainerUtil.getOnlyItem(SimpleUtil.findProperties(project, key));
          if (simpleProperty != null) {
            // Add a folding descriptor for the literal expression at this node.
            descriptors.add(new FoldingDescriptor(literalExpression.getNode(),
                new TextRange(literalExpression.getTextRange().getStartOffset() + 1,
                    literalExpression.getTextRange().getEndOffset() - 1),
                group, Collections.singleton(simpleProperty)));
          }
        }
      }
    });

    return descriptors.toArray(FoldingDescriptor.EMPTY_ARRAY);
  }

  /**
   * Gets the Simple Language 'value' string corresponding to the 'key'
   *
   * @param node Node corresponding to PsiLiteralExpression containing a string in the format
   *             SIMPLE_PREFIX_STR + SIMPLE_SEPARATOR_STR + Key, where Key is
   *             defined by the Simple language file.
   */
  @Nullable
  @Override
  public String getPlaceholderText(@NotNull ASTNode node) {
    if (node.getPsi() instanceof PsiLiteralExpression psiLiteralExpression) {
      String text = PsiLiteralUtil.getStringLiteralContent(psiLiteralExpression);
      if (text == null) {
        return null;
      }

      String key = text.substring(SimpleAnnotator.SIMPLE_PREFIX_STR.length() +
          SimpleAnnotator.SIMPLE_SEPARATOR_STR.length());

      SimpleProperty simpleProperty = ContainerUtil.getOnlyItem(
          SimpleUtil.findProperties(psiLiteralExpression.getProject(), key)
      );
      if (simpleProperty == null) {
        return StringUtil.THREE_DOTS;
      }

      String propertyValue = simpleProperty.getValue();
      // IMPORTANT: keys can come with no values, so a test for null is needed
      // IMPORTANT: Convert embedded \n to backslash n, so that the string will look
      // like it has LF embedded in it and embedded " to escaped "
      if (propertyValue == null) {
        return StringUtil.THREE_DOTS;
      }

      return propertyValue
          .replaceAll("\n", "\\n")
          .replaceAll("\"", "\\\\\"");
    }

    return null;
  }

  @Override
  public boolean isCollapsedByDefault(@NotNull ASTNode node) {
    return true;
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleFileType.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.openapi.fileTypes.LanguageFileType;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

public final class SimpleFileType extends LanguageFileType {

  public static final SimpleFileType INSTANCE = new SimpleFileType();

  private SimpleFileType() {
    super(SimpleLanguage.INSTANCE);
  }

  @NotNull
  @Override
  public String getName() {
    return "Simple File";
  }

  @NotNull
  @Override
  public String getDescription() {
    return "Simple language file";
  }

  @NotNull
  @Override
  public String getDefaultExtension() {
    return "simple";
  }

  @Override
  public Icon getIcon() {
    return SimpleIcons.FILE;
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleChooseByNameContributor.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.navigation.ChooseByNameContributorEx;
import com.intellij.navigation.NavigationItem;
import com.intellij.openapi.project.Project;
import com.intellij.psi.search.GlobalSearchScope;
import com.intellij.util.Processor;
import com.intellij.util.containers.ContainerUtil;
import com.intellij.util.indexing.FindSymbolParameters;
import com.intellij.util.indexing.IdFilter;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.List;
import java.util.Objects;

final class SimpleChooseByNameContributor implements ChooseByNameContributorEx {

  @Override
  public void processNames(@NotNull Processor<? super String> processor,
                           @NotNull GlobalSearchScope scope,
                           @Nullable IdFilter filter) {
    Project project = Objects.requireNonNull(scope.getProject());
    List<String> propertyKeys = ContainerUtil.map(
        SimpleUtil.findProperties(project), SimpleProperty::getKey);
    ContainerUtil.process(propertyKeys, processor);
  }

  @Override
  public void processElementsWithName(@NotNull String name,
                                      @NotNull Processor<? super NavigationItem> processor,
                                      @NotNull FindSymbolParameters parameters) {
    List<NavigationItem> properties = ContainerUtil.map(
        SimpleUtil.findProperties(parameters.getProject(), name),
        property -> (NavigationItem) property);
    ContainerUtil.process(properties, processor);
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleStructureViewElement.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.ide.projectView.PresentationData;
import com.intellij.ide.structureView.StructureViewTreeElement;
import com.intellij.ide.util.treeView.smartTree.SortableTreeElement;
import com.intellij.ide.util.treeView.smartTree.TreeElement;
import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.NavigatablePsiElement;
import com.intellij.psi.util.PsiTreeUtil;
import org.intellij.sdk.language.psi.SimpleFile;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.intellij.sdk.language.psi.impl.SimplePropertyImpl;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;

public class SimpleStructureViewElement implements StructureViewTreeElement, SortableTreeElement {

  private final NavigatablePsiElement myElement;

  public SimpleStructureViewElement(NavigatablePsiElement element) {
    this.myElement = element;
  }

  @Override
  public Object getValue() {
    return myElement;
  }

  @Override
  public void navigate(boolean requestFocus) {
    myElement.navigate(requestFocus);
  }

  @Override
  public boolean canNavigate() {
    return myElement.canNavigate();
  }

  @Override
  public boolean canNavigateToSource() {
    return myElement.canNavigateToSource();
  }

  @NotNull
  @Override
  public String getAlphaSortKey() {
    String name = myElement.getName();
    return name != null ? name : "";
  }

  @NotNull
  @Override
  public ItemPresentation getPresentation() {
    ItemPresentation presentation = myElement.getPresentation();
    return presentation != null ? presentation : new PresentationData();
  }

  @Override
  public TreeElement @NotNull [] getChildren() {
    if (myElement instanceof SimpleFile) {
      List<SimpleProperty> properties = PsiTreeUtil.getChildrenOfTypeAsList(myElement, SimpleProperty.class);
      List<TreeElement> treeElements = new ArrayList<>(properties.size());
      for (SimpleProperty property : properties) {
        treeElements.add(new SimpleStructureViewElement((SimplePropertyImpl) property));
      }
      return treeElements.toArray(new TreeElement[0]);
    }
    return EMPTY_ARRAY;
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleStructureAwareNavbar.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.icons.AllIcons;
import com.intellij.ide.navigationToolbar.StructureAwareNavBarModelExtension;
import com.intellij.lang.Language;
import org.intellij.sdk.language.psi.SimpleFile;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.Icon;

final class SimpleStructureAwareNavbar extends StructureAwareNavBarModelExtension {

  @NotNull
  @Override
  protected Language getLanguage() {
    return SimpleLanguage.INSTANCE;
  }

  @Override
  public @Nullable String getPresentableText(Object object) {
    if (object instanceof SimpleFile) {
      return ((SimpleFile) object).getName();
    }
    if (object instanceof SimpleProperty) {
      return ((SimpleProperty) object).getName();
    }

    return null;
  }

  @Override
  @Nullable
  public Icon getIcon(Object object) {
    if (object instanceof SimpleProperty) {
      return AllIcons.Nodes.Property;
    }

    return null;
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleSyntaxHighlighter.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.lexer.Lexer;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.HighlighterColors;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.psi.TokenType;
import com.intellij.psi.tree.IElementType;
import org.intellij.sdk.language.psi.SimpleTypes;
import org.jetbrains.annotations.NotNull;

import static com.intellij.openapi.editor.colors.TextAttributesKey.createTextAttributesKey;

public class SimpleSyntaxHighlighter extends SyntaxHighlighterBase {

  public static final TextAttributesKey SEPARATOR =
      createTextAttributesKey("SIMPLE_SEPARATOR", DefaultLanguageHighlighterColors.OPERATION_SIGN);
  public static final TextAttributesKey KEY =
      createTextAttributesKey("SIMPLE_KEY", DefaultLanguageHighlighterColors.KEYWORD);
  public static final TextAttributesKey VALUE =
      createTextAttributesKey("SIMPLE_VALUE", DefaultLanguageHighlighterColors.STRING);
  public static final TextAttributesKey COMMENT =
      createTextAttributesKey("SIMPLE_COMMENT", DefaultLanguageHighlighterColors.LINE_COMMENT);
  public static final TextAttributesKey BAD_CHARACTER =
      createTextAttributesKey("SIMPLE_BAD_CHARACTER", HighlighterColors.BAD_CHARACTER);


  private static final TextAttributesKey[] BAD_CHAR_KEYS = new TextAttributesKey[]{BAD_CHARACTER};
  private static final TextAttributesKey[] SEPARATOR_KEYS = new TextAttributesKey[]{SEPARATOR};
  private static final TextAttributesKey[] KEY_KEYS = new TextAttributesKey[]{KEY};
  private static final TextAttributesKey[] VALUE_KEYS = new TextAttributesKey[]{VALUE};
  private static final TextAttributesKey[] COMMENT_KEYS = new TextAttributesKey[]{COMMENT};
  private static final TextAttributesKey[] EMPTY_KEYS = new TextAttributesKey[0];

  @NotNull
  @Override
  public Lexer getHighlightingLexer() {
    return new SimpleLexerAdapter();
  }

  @Override
  public TextAttributesKey @NotNull [] getTokenHighlights(IElementType tokenType) {
    if (tokenType.equals(SimpleTypes.SEPARATOR)) {
      return SEPARATOR_KEYS;
    }
    if (tokenType.equals(SimpleTypes.KEY)) {
      return KEY_KEYS;
    }
    if (tokenType.equals(SimpleTypes.VALUE)) {
      return VALUE_KEYS;
    }
    if (tokenType.equals(SimpleTypes.COMMENT)) {
      return COMMENT_KEYS;
    }
    if (tokenType.equals(TokenType.BAD_CHARACTER)) {
      return BAD_CHAR_KEYS;
    }
    return EMPTY_KEYS;
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleRefactoringSupportProvider.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.lang.refactoring.RefactoringSupportProvider;
import com.intellij.psi.PsiElement;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

final class SimpleRefactoringSupportProvider extends RefactoringSupportProvider {

  @Override
  public boolean isMemberInplaceRenameAvailable(@NotNull PsiElement elementToRename, @Nullable PsiElement context) {
    return (elementToRename instanceof SimpleProperty);
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleColorSettingsPage.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.fileTypes.SyntaxHighlighter;
import com.intellij.openapi.options.colors.AttributesDescriptor;
import com.intellij.openapi.options.colors.ColorDescriptor;
import com.intellij.openapi.options.colors.ColorSettingsPage;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.util.Map;

final class SimpleColorSettingsPage implements ColorSettingsPage {

  private static final AttributesDescriptor[] DESCRIPTORS = new AttributesDescriptor[]{
      new AttributesDescriptor("Key", SimpleSyntaxHighlighter.KEY),
      new AttributesDescriptor("Separator", SimpleSyntaxHighlighter.SEPARATOR),
      new AttributesDescriptor("Value", SimpleSyntaxHighlighter.VALUE),
      new AttributesDescriptor("Bad value", SimpleSyntaxHighlighter.BAD_CHARACTER)
  };

  @Override
  public Icon getIcon() {
    return SimpleIcons.FILE;
  }

  @NotNull
  @Override
  public SyntaxHighlighter getHighlighter() {
    return new SimpleSyntaxHighlighter();
  }

  @NotNull
  @Override
  public String getDemoText() {
    return """
        # You are reading the ".properties" entry.
        ! The exclamation mark can also mark text as comments.
        website = https://en.wikipedia.org/
        language = English
        # The backslash below tells the application to continue reading
        # the value onto the next line.
        message = Welcome to \\
                  Wikipedia!
        # Add spaces to the key
        key\\ with\\ spaces = This is the value that could be looked up with the key "key with spaces".
        # Unicode
        tab : \\u0009""";
  }

  @Nullable
  @Override
  public Map<String, TextAttributesKey> getAdditionalHighlightingTagToDescriptorMap() {
    return null;
  }

  @Override
  public AttributesDescriptor @NotNull [] getAttributeDescriptors() {
    return DESCRIPTORS;
  }

  @Override
  public ColorDescriptor @NotNull [] getColorDescriptors() {
    return ColorDescriptor.EMPTY_ARRAY;
  }

  @NotNull
  @Override
  public String getDisplayName() {
    return "Simple";
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleIcons.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.openapi.util.IconLoader;

import javax.swing.*;

public class SimpleIcons {

  public static final Icon FILE = IconLoader.getIcon("/icons/jar-gray.png", SimpleIcons.class);

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleParserDefinition.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.lang.ASTNode;
import com.intellij.lang.ParserDefinition;
import com.intellij.lang.PsiParser;
import com.intellij.lexer.Lexer;
import com.intellij.openapi.project.Project;
import com.intellij.psi.FileViewProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.tree.IFileElementType;
import com.intellij.psi.tree.TokenSet;
import org.intellij.sdk.language.parser.SimpleParser;
import org.intellij.sdk.language.psi.SimpleFile;
import org.intellij.sdk.language.psi.SimpleTokenSets;
import org.intellij.sdk.language.psi.SimpleTypes;
import org.jetbrains.annotations.NotNull;

final class SimpleParserDefinition implements ParserDefinition {

  public static final IFileElementType FILE = new IFileElementType(SimpleLanguage.INSTANCE);

  @NotNull
  @Override
  public Lexer createLexer(Project project) {
    return new SimpleLexerAdapter();
  }

  @NotNull
  @Override
  public TokenSet getCommentTokens() {
    return SimpleTokenSets.COMMENTS;
  }

  @NotNull
  @Override
  public TokenSet getStringLiteralElements() {
    return TokenSet.EMPTY;
  }

  @NotNull
  @Override
  public PsiParser createParser(final Project project) {
    return new SimpleParser();
  }

  @NotNull
  @Override
  public IFileElementType getFileNodeType() {
    return FILE;
  }

  @NotNull
  @Override
  public PsiFile createFile(@NotNull FileViewProvider viewProvider) {
    return new SimpleFile(viewProvider);
  }

  @NotNull
  @Override
  public PsiElement createElement(ASTNode node) {
    return SimpleTypes.Factory.createElement(node);
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleAnnotator.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.codeInspection.ProblemHighlightType;
import com.intellij.lang.annotation.AnnotationHolder;
import com.intellij.lang.annotation.Annotator;
import com.intellij.lang.annotation.HighlightSeverity;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiLiteralExpression;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;

import java.util.List;

final class SimpleAnnotator implements Annotator {

  // Define strings for the Simple language prefix - used for annotations, line markers, etc.
  public static final String SIMPLE_PREFIX_STR = "simple";
  public static final String SIMPLE_SEPARATOR_STR = ":";

  @Override
  public void annotate(@NotNull final PsiElement element, @NotNull AnnotationHolder holder) {
    // Ensure the PSI Element is an expression
    if (!(element instanceof PsiLiteralExpression literalExpression)) {
      return;
    }

    // Ensure the PSI element contains a string that starts with the prefix and separator
    String value = literalExpression.getValue() instanceof String ? (String) literalExpression.getValue() : null;
    if (value == null || !value.startsWith(SIMPLE_PREFIX_STR + SIMPLE_SEPARATOR_STR)) {
      return;
    }

    // Define the text ranges (start is inclusive, end is exclusive)
    // "simple:key"
    //  01234567890
    TextRange prefixRange = TextRange.from(element.getTextRange().getStartOffset(), SIMPLE_PREFIX_STR.length() + 1);
    TextRange separatorRange = TextRange.from(prefixRange.getEndOffset(), SIMPLE_SEPARATOR_STR.length());
    TextRange keyRange = new TextRange(separatorRange.getEndOffset(), element.getTextRange().getEndOffset() - 1);

    // highlight "simple" prefix and ":" separator
    holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
        .range(prefixRange).textAttributes(DefaultLanguageHighlighterColors.KEYWORD).create();
    holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
        .range(separatorRange).textAttributes(SimpleSyntaxHighlighter.SEPARATOR).create();


    // Get the list of properties for given key
    String key = value.substring(SIMPLE_PREFIX_STR.length() + SIMPLE_SEPARATOR_STR.length());
    List<SimpleProperty> properties = SimpleUtil.findProperties(element.getProject(), key);
    if (properties.isEmpty()) {
      holder.newAnnotation(HighlightSeverity.ERROR, "Unresolved property")
          .range(keyRange)
          .highlightType(ProblemHighlightType.LIKE_UNKNOWN_SYMBOL)
          // ** Tutorial step 19. - Add a quick fix for the string containing possible properties
          .withFix(new SimpleCreatePropertyQuickFix(key))
          .create();
    } else {
      // Found at least one property, force the text attributes to Simple syntax value character
      holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
          .range(keyRange).textAttributes(SimpleSyntaxHighlighter.VALUE).create();
    }
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleBlock.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.formatting.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.TokenType;
import com.intellij.psi.formatter.common.AbstractBlock;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class SimpleBlock extends AbstractBlock {

  private final SpacingBuilder spacingBuilder;

  protected SimpleBlock(@NotNull ASTNode node, @Nullable Wrap wrap, @Nullable Alignment alignment,
                        SpacingBuilder spacingBuilder) {
    super(node, wrap, alignment);
    this.spacingBuilder = spacingBuilder;
  }

  @Override
  protected List<Block> buildChildren() {
    List<Block> blocks = new ArrayList<>();
    ASTNode child = myNode.getFirstChildNode();
    while (child != null) {
      if (child.getElementType() != TokenType.WHITE_SPACE) {
        Block block = new SimpleBlock(child, Wrap.createWrap(WrapType.NONE, false), Alignment.createAlignment(),
            spacingBuilder);
        blocks.add(block);
      }
      child = child.getTreeNext();
    }
    return blocks;
  }

  @Override
  public Indent getIndent() {
    return Indent.getNoneIndent();
  }

  @Nullable
  @Override
  public Spacing getSpacing(@Nullable Block child1, @NotNull Block child2) {
    return spacingBuilder.getSpacing(this, child1, child2);
  }

  @Override
  public boolean isLeaf() {
    return myNode.getFirstChildNode() == null;
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleReferenceContributor.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.openapi.util.TextRange;
import com.intellij.patterns.PlatformPatterns;
import com.intellij.psi.*;
import com.intellij.util.ProcessingContext;
import org.jetbrains.annotations.NotNull;

import static org.intellij.sdk.language.SimpleAnnotator.SIMPLE_PREFIX_STR;
import static org.intellij.sdk.language.SimpleAnnotator.SIMPLE_SEPARATOR_STR;

final class SimpleReferenceContributor extends PsiReferenceContributor {

  @Override
  public void registerReferenceProviders(@NotNull PsiReferenceRegistrar registrar) {
    registrar.registerReferenceProvider(PlatformPatterns.psiElement(PsiLiteralExpression.class),
        new PsiReferenceProvider() {
          @Override
          public PsiReference @NotNull [] getReferencesByElement(@NotNull PsiElement element,
                                                                 @NotNull ProcessingContext context) {
            PsiLiteralExpression literalExpression = (PsiLiteralExpression) element;
            String value = literalExpression.getValue() instanceof String ?
                (String) literalExpression.getValue() : null;
            if ((value != null && value.startsWith(SIMPLE_PREFIX_STR + SIMPLE_SEPARATOR_STR))) {
              TextRange property = new TextRange(SIMPLE_PREFIX_STR.length() + SIMPLE_SEPARATOR_STR.length() + 1,
                  value.length() + 1);
              return new PsiReference[]{new SimpleReference(element, property)};
            }
            return PsiReference.EMPTY_ARRAY;
          }
        });
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleSyntaxHighlighterFactory.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.openapi.fileTypes.SyntaxHighlighter;
import com.intellij.openapi.fileTypes.SyntaxHighlighterFactory;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.VirtualFile;
import org.jetbrains.annotations.NotNull;

final class SimpleSyntaxHighlighterFactory extends SyntaxHighlighterFactory {

  @NotNull
  @Override
  public SyntaxHighlighter getSyntaxHighlighter(Project project, VirtualFile virtualFile) {
    return new SimpleSyntaxHighlighter();
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleCompletionContributor.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.codeInsight.completion.*;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.patterns.PlatformPatterns;
import com.intellij.util.ProcessingContext;
import org.intellij.sdk.language.psi.SimpleTypes;
import org.jetbrains.annotations.NotNull;

final class SimpleCompletionContributor extends CompletionContributor {

  SimpleCompletionContributor() {
    extend(CompletionType.BASIC, PlatformPatterns.psiElement(SimpleTypes.VALUE),
        new CompletionProvider<>() {
          public void addCompletions(@NotNull CompletionParameters parameters,
                                     @NotNull ProcessingContext context,
                                     @NotNull CompletionResultSet resultSet) {
            resultSet.addElement(LookupElementBuilder.create("Hello"));
          }
        }
    );
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleReference.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementResolveResult;
import com.intellij.psi.PsiPolyVariantReferenceBase;
import com.intellij.psi.ResolveResult;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;

final class SimpleReference extends PsiPolyVariantReferenceBase<PsiElement> {

  private final String key;

  SimpleReference(@NotNull PsiElement element, TextRange textRange) {
    super(element, textRange);
    key = element.getText()
        .substring(textRange.getStartOffset(), textRange.getEndOffset());
  }

  @Override
  public ResolveResult @NotNull [] multiResolve(boolean incompleteCode) {
    Project project = myElement.getProject();
    List<SimpleProperty> properties = SimpleUtil.findProperties(project, key);
    List<ResolveResult> results = new ArrayList<>();
    for (SimpleProperty property : properties) {
      results.add(new PsiElementResolveResult(property));
    }
    return results.toArray(new ResolveResult[0]);
  }

  @Override
  public Object @NotNull [] getVariants() {
    Project project = myElement.getProject();
    List<SimpleProperty> properties = SimpleUtil.findProperties(project);
    List<LookupElement> variants = new ArrayList<>();
    for (SimpleProperty property : properties) {
      if (property.getKey() != null && !property.getKey().isEmpty()) {
        variants.add(LookupElementBuilder
            .create(property).withIcon(SimpleIcons.FILE)
            .withTypeText(property.getContainingFile().getName())
        );
      }
    }
    return variants.toArray();
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/psi/impl/SimplePsiImplUtil.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language.psi.impl;

import com.intellij.lang.ASTNode;
import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import org.intellij.sdk.language.psi.SimpleElementFactory;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.intellij.sdk.language.psi.SimpleTypes;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

public class SimplePsiImplUtil {

  public static String getKey(SimpleProperty element) {
    ASTNode keyNode = element.getNode().findChildByType(SimpleTypes.KEY);
    if (keyNode != null) {
      // IMPORTANT: Convert embedded escaped spaces to simple spaces
      return keyNode.getText().replaceAll("\\\\ ", " ");
    } else {
      return null;
    }
  }

  public static String getValue(SimpleProperty element) {
    ASTNode valueNode = element.getNode().findChildByType(SimpleTypes.VALUE);
    if (valueNode != null) {
      return valueNode.getText();
    } else {
      return null;
    }
  }

  public static String getName(SimpleProperty element) {
    return getKey(element);
  }

  public static PsiElement setName(SimpleProperty element, String newName) {
    ASTNode keyNode = element.getNode().findChildByType(SimpleTypes.KEY);
    if (keyNode != null) {
      SimpleProperty property = SimpleElementFactory.createProperty(element.getProject(), newName);
      ASTNode newKeyNode = property.getFirstChild().getNode();
      element.getNode().replaceChild(keyNode, newKeyNode);
    }
    return element;
  }

  public static PsiElement getNameIdentifier(SimpleProperty element) {
    ASTNode keyNode = element.getNode().findChildByType(SimpleTypes.KEY);
    if (keyNode != null) {
      return keyNode.getPsi();
    } else {
      return null;
    }
  }

  public static ItemPresentation getPresentation(final SimpleProperty element) {
    return new ItemPresentation() {
      @Nullable
      @Override
      public String getPresentableText() {
        return element.getKey();
      }

      @Nullable
      @Override
      public String getLocationString() {
        PsiFile containingFile = element.getContainingFile();
        return containingFile == null ? null : containingFile.getName();
      }

      @Override
      public Icon getIcon(boolean unused) {
        return element.getIcon(0);
      }
    };
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/psi/impl/SimpleNamedElementImpl.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language.psi.impl;

import com.intellij.extapi.psi.ASTWrapperPsiElement;
import com.intellij.lang.ASTNode;
import org.intellij.sdk.language.psi.SimpleNamedElement;
import org.jetbrains.annotations.NotNull;

public abstract class SimpleNamedElementImpl extends ASTWrapperPsiElement implements SimpleNamedElement {

  public SimpleNamedElementImpl(@NotNull ASTNode node) {
    super(node);
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/psi/SimpleNamedElement.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language.psi;

import com.intellij.psi.PsiNameIdentifierOwner;

public interface SimpleNamedElement extends PsiNameIdentifierOwner {

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/psi/SimpleElementFactory.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language.psi;

import com.intellij.openapi.project.Project;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFileFactory;
import org.intellij.sdk.language.SimpleFileType;

public class SimpleElementFactory {

  public static SimpleProperty createProperty(Project project, String name) {
    final SimpleFile file = createFile(project, name);
    return (SimpleProperty) file.getFirstChild();
  }

  public static SimpleFile createFile(Project project, String text) {
    String name = "dummy.simple";
    return (SimpleFile) PsiFileFactory.getInstance(project).createFileFromText(name, SimpleFileType.INSTANCE, text);
  }

  public static SimpleProperty createProperty(Project project, String name, String value) {
    final SimpleFile file = createFile(project, name + " = " + value);
    return (SimpleProperty) file.getFirstChild();
  }

  public static PsiElement createCRLF(Project project) {
    final SimpleFile file = createFile(project, "\n");
    return file.getFirstChild();
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/psi/SimpleFile.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language.psi;

import com.intellij.extapi.psi.PsiFileBase;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.FileViewProvider;
import org.intellij.sdk.language.SimpleFileType;
import org.intellij.sdk.language.SimpleLanguage;
import org.jetbrains.annotations.NotNull;

public class SimpleFile extends PsiFileBase {

  public SimpleFile(@NotNull FileViewProvider viewProvider) {
    super(viewProvider, SimpleLanguage.INSTANCE);
  }

  @NotNull
  @Override
  public FileType getFileType() {
    return SimpleFileType.INSTANCE;
  }

  @Override
  public String toString() {
    return "Simple File";
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/psi/SimpleElementType.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language.psi;

import com.intellij.psi.tree.IElementType;
import org.intellij.sdk.language.SimpleLanguage;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class SimpleElementType extends IElementType {

  public SimpleElementType(@NotNull @NonNls String debugName) {
    super(debugName, SimpleLanguage.INSTANCE);
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/psi/SimpleTokenSets.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language.psi;

import com.intellij.psi.tree.TokenSet;

public interface SimpleTokenSets {

  TokenSet IDENTIFIERS = TokenSet.create(SimpleTypes.KEY);

  TokenSet COMMENTS = TokenSet.create(SimpleTypes.COMMENT);

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/psi/SimpleTokenType.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language.psi;

import com.intellij.psi.tree.IElementType;
import org.intellij.sdk.language.SimpleLanguage;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

public class SimpleTokenType extends IElementType {

  public SimpleTokenType(@NotNull @NonNls String debugName) {
    super(debugName, SimpleLanguage.INSTANCE);
  }

  @Override
  public String toString() {
    return "SimpleTokenType." + super.toString();
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleUtil.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.google.common.collect.Lists;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.text.StringUtil;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.psi.PsiComment;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiManager;
import com.intellij.psi.PsiWhiteSpace;
import com.intellij.psi.search.FileTypeIndex;
import com.intellij.psi.search.GlobalSearchScope;
import com.intellij.psi.util.PsiTreeUtil;
import org.intellij.sdk.language.psi.SimpleFile;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;

import java.util.*;

public class SimpleUtil {

  /**
   * Searches the entire project for Simple language files with instances of the Simple property with the given key.
   *
   * @param project current project
   * @param key     to check
   * @return matching properties
   */
  public static List<SimpleProperty> findProperties(Project project, String key) {
    List<SimpleProperty> result = new ArrayList<>();
    Collection<VirtualFile> virtualFiles =
        FileTypeIndex.getFiles(SimpleFileType.INSTANCE, GlobalSearchScope.allScope(project));
    for (VirtualFile virtualFile : virtualFiles) {
      SimpleFile simpleFile = (SimpleFile) PsiManager.getInstance(project).findFile(virtualFile);
      if (simpleFile != null) {
        SimpleProperty[] properties = PsiTreeUtil.getChildrenOfType(simpleFile, SimpleProperty.class);
        if (properties != null) {
          for (SimpleProperty property : properties) {
            if (key.equals(property.getKey())) {
              result.add(property);
            }
          }
        }
      }
    }
    return result;
  }

  public static List<SimpleProperty> findProperties(Project project) {
    List<SimpleProperty> result = new ArrayList<>();
    Collection<VirtualFile> virtualFiles =
        FileTypeIndex.getFiles(SimpleFileType.INSTANCE, GlobalSearchScope.allScope(project));
    for (VirtualFile virtualFile : virtualFiles) {
      SimpleFile simpleFile = (SimpleFile) PsiManager.getInstance(project).findFile(virtualFile);
      if (simpleFile != null) {
        SimpleProperty[] properties = PsiTreeUtil.getChildrenOfType(simpleFile, SimpleProperty.class);
        if (properties != null) {
          Collections.addAll(result, properties);
        }
      }
    }
    return result;
  }

  /**
   * Attempts to collect any comment elements above the Simple key/value pair.
   */
  public static @NotNull String findDocumentationComment(SimpleProperty property) {
    List<String> result = new LinkedList<>();
    PsiElement element = property.getPrevSibling();
    while (element instanceof PsiComment || element instanceof PsiWhiteSpace) {
      if (element instanceof PsiComment) {
        String commentText = element.getText().replaceFirst("[!# ]+", "");
        result.add(commentText);
      }
      element = element.getPrevSibling();
    }
    return StringUtil.join(Lists.reverse(result), "\n ");
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleLanguage.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.lang.Language;

public class SimpleLanguage extends Language {

  public static final SimpleLanguage INSTANCE = new SimpleLanguage();

  private SimpleLanguage() {
    super("Simple");
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimplePropertyIconProvider.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

package org.intellij.sdk.language;

import com.intellij.ide.IconProvider;
import com.intellij.psi.PsiElement;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

final class SimplePropertyIconProvider extends IconProvider {

  @Override
  public @Nullable Icon getIcon(@NotNull PsiElement element, int flags) {
    return element instanceof SimpleProperty ? SimpleIcons.FILE : null;
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleFormattingModelBuilder.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.language;

import com.intellij.formatting.*;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import org.intellij.sdk.language.psi.SimpleTypes;
import org.jetbrains.annotations.NotNull;

final class SimpleFormattingModelBuilder implements FormattingModelBuilder {

  private static SpacingBuilder createSpaceBuilder(CodeStyleSettings settings) {
    return new SpacingBuilder(settings, SimpleLanguage.INSTANCE)
        .around(SimpleTypes.SEPARATOR)
        .spaceIf(settings.getCommonSettings(SimpleLanguage.INSTANCE.getID()).SPACE_AROUND_ASSIGNMENT_OPERATORS)
        .before(SimpleTypes.PROPERTY)
        .none();
  }

  @Override
  public @NotNull FormattingModel createModel(@NotNull FormattingContext formattingContext) {
    final CodeStyleSettings codeStyleSettings = formattingContext.getCodeStyleSettings();
    return FormattingModelProvider
        .createFormattingModelForPsiFile(formattingContext.getContainingFile(),
            new SimpleBlock(formattingContext.getNode(),
                Wrap.createWrap(WrapType.NONE, false),
                Alignment.createAlignment(),
                createSpaceBuilder(codeStyleSettings)),
            codeStyleSettings);
  }

}

```

# simple_language_plugin/src/main/java/org/intellij/sdk/language/SimpleDocumentationProvider.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.
package org.intellij.sdk.language;

import com.intellij.lang.documentation.AbstractDocumentationProvider;
import com.intellij.lang.documentation.DocumentationMarkup;
import com.intellij.psi.PsiElement;
import com.intellij.psi.presentation.java.SymbolPresentationUtil;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.List;

/**
 * TODO Please note, it is recommended to utilize the new DocumentationTarget API for
 * plugins targeting IntelliJ Platform version 2023.1 or later.
 *
 * @see <a href="https://plugins.jetbrains.com/docs/intellij/documentation.html">Documentation (IntelliJ Platform Docs)</a>
 */
final class SimpleDocumentationProvider extends AbstractDocumentationProvider {

  /**
   * For the Simple Language, we don't have online documentation. However, if your language provides
   * references pages online, URLs for the element can be returned here.
   */
  @Override
  public @Nullable List<String> getUrlFor(PsiElement element, PsiElement originalElement) {
    return null;
  }

  /**
   * Extracts the key, value, file and documentation comment of a Simple key/value entry and returns
   * a formatted representation of the information.
   */
  @Override
  public @Nullable String generateDoc(PsiElement element, @Nullable PsiElement originalElement) {
    if (element instanceof SimpleProperty) {
      final String key = ((SimpleProperty) element).getKey();
      final String value = ((SimpleProperty) element).getValue();
      final String file = SymbolPresentationUtil.getFilePathPresentation(element.getContainingFile());
      final String docComment = SimpleUtil.findDocumentationComment((SimpleProperty) element);

      return renderFullDoc(key, value, file, docComment);
    }
    return null;
  }

  /**
   * Provides the information in which file the Simple language key/value is defined.
   */
  @Override
  public @Nullable String getQuickNavigateInfo(PsiElement element, PsiElement originalElement) {
    if (element instanceof SimpleProperty) {
      final String key = ((SimpleProperty) element).getKey();
      final String file = SymbolPresentationUtil.getFilePathPresentation(element.getContainingFile());
      return "\"" + key + "\" in " + file;
    }
    return null;
  }

  /**
   * Provides documentation when a Simple Language element is hovered with the mouse.
   */
  @Override
  public @Nullable String generateHoverDoc(@NotNull PsiElement element, @Nullable PsiElement originalElement) {
    return generateDoc(element, originalElement);
  }

  /**
   * Creates a key/value row for the rendered documentation.
   */
  private void addKeyValueSection(String key, String value, StringBuilder sb) {
    sb.append(DocumentationMarkup.SECTION_HEADER_START);
    sb.append(key);
    sb.append(DocumentationMarkup.SECTION_SEPARATOR);
    sb.append("<p>");
    sb.append(value);
    sb.append(DocumentationMarkup.SECTION_END);
  }

  /**
   * Creates the formatted documentation using {@link DocumentationMarkup}. See the Java doc of
   * {@link com.intellij.lang.documentation.DocumentationProvider#generateDoc(PsiElement, PsiElement)} for more
   * information about building the layout.
   */
  private String renderFullDoc(String key, String value, String file, String docComment) {
    StringBuilder sb = new StringBuilder();
    sb.append(DocumentationMarkup.DEFINITION_START);
    sb.append("Simple Property");
    sb.append(DocumentationMarkup.DEFINITION_END);
    sb.append(DocumentationMarkup.CONTENT_START);
    sb.append(value);
    sb.append(DocumentationMarkup.CONTENT_END);
    sb.append(DocumentationMarkup.SECTIONS_START);
    addKeyValueSection("Key:", key, sb);
    addKeyValueSection("Value:", value, sb);
    addKeyValueSection("File:", file, sb);
    addKeyValueSection("Comment:", docComment, sb);
    sb.append(DocumentationMarkup.SECTIONS_END);
    return sb.toString();
  }

}

```

# simple_language_plugin/src/main/gen/org/intellij/sdk/language/parser/SimpleParser.java
```java
// This is a generated file. Not intended for manual editing.
package org.intellij.sdk.language.parser;

import com.intellij.lang.ASTNode;
import com.intellij.lang.LightPsiParser;
import com.intellij.lang.PsiBuilder;
import com.intellij.lang.PsiBuilder.Marker;
import com.intellij.lang.PsiParser;
import com.intellij.psi.tree.IElementType;

import static com.intellij.lang.parser.GeneratedParserUtilBase.*;
import static org.intellij.sdk.language.psi.SimpleTypes.*;

@SuppressWarnings({"SimplifiableIfStatement", "UnusedAssignment"})
public class SimpleParser implements PsiParser, LightPsiParser {

  public ASTNode parse(IElementType t, PsiBuilder b) {
    parseLight(t, b);
    return b.getTreeBuilt();
  }

  public void parseLight(IElementType t, PsiBuilder b) {
    boolean r;
    b = adapt_builder_(t, b, this, null);
    Marker m = enter_section_(b, 0, _COLLAPSE_, null);
    r = parse_root_(t, b);
    exit_section_(b, 0, m, t, r, true, TRUE_CONDITION);
  }

  protected boolean parse_root_(IElementType t, PsiBuilder b) {
    return parse_root_(t, b, 0);
  }

  static boolean parse_root_(IElementType t, PsiBuilder b, int l) {
    return simpleFile(b, l + 1);
  }

  /* ********************************************************** */
  // property|COMMENT|CRLF
  static boolean item_(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "item_")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = property(b, l + 1);
    if (!r) r = consumeToken(b, COMMENT);
    if (!r) r = consumeToken(b, CRLF);
    exit_section_(b, m, null, r);
    return r;
  }

  /* ********************************************************** */
  // (KEY? SEPARATOR VALUE?) | KEY
  public static boolean property(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "property")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NONE_, PROPERTY, "<property>");
    r = property_0(b, l + 1);
    if (!r) r = consumeToken(b, KEY);
    exit_section_(b, l, m, r, false, SimpleParser::recover_property);
    return r;
  }

  // KEY? SEPARATOR VALUE?
  private static boolean property_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "property_0")) return false;
    boolean r;
    Marker m = enter_section_(b);
    r = property_0_0(b, l + 1);
    r = r && consumeToken(b, SEPARATOR);
    r = r && property_0_2(b, l + 1);
    exit_section_(b, m, null, r);
    return r;
  }

  // KEY?
  private static boolean property_0_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "property_0_0")) return false;
    consumeToken(b, KEY);
    return true;
  }

  // VALUE?
  private static boolean property_0_2(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "property_0_2")) return false;
    consumeToken(b, VALUE);
    return true;
  }

  /* ********************************************************** */
  // !(KEY|SEPARATOR|COMMENT)
  static boolean recover_property(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "recover_property")) return false;
    boolean r;
    Marker m = enter_section_(b, l, _NOT_);
    r = !recover_property_0(b, l + 1);
    exit_section_(b, l, m, r, false, null);
    return r;
  }

  // KEY|SEPARATOR|COMMENT
  private static boolean recover_property_0(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "recover_property_0")) return false;
    boolean r;
    r = consumeToken(b, KEY);
    if (!r) r = consumeToken(b, SEPARATOR);
    if (!r) r = consumeToken(b, COMMENT);
    return r;
  }

  /* ********************************************************** */
  // item_*
  static boolean simpleFile(PsiBuilder b, int l) {
    if (!recursion_guard_(b, l, "simpleFile")) return false;
    while (true) {
      int c = current_position_(b);
      if (!item_(b, l + 1)) break;
      if (!empty_element_parsed_guard_(b, "simpleFile", c)) break;
    }
    return true;
  }

}

```

# simple_language_plugin/src/main/gen/org/intellij/sdk/language/psi/impl/SimplePropertyImpl.java
```java
// This is a generated file. Not intended for manual editing.
package org.intellij.sdk.language.psi.impl;

import com.intellij.lang.ASTNode;
import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import org.intellij.sdk.language.psi.SimpleProperty;
import org.intellij.sdk.language.psi.SimpleVisitor;
import org.jetbrains.annotations.NotNull;

public class SimplePropertyImpl extends SimpleNamedElementImpl implements SimpleProperty {

  public SimplePropertyImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull SimpleVisitor visitor) {
    visitor.visitProperty(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof SimpleVisitor) accept((SimpleVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  public String getKey() {
    return SimplePsiImplUtil.getKey(this);
  }

  @Override
  public String getValue() {
    return SimplePsiImplUtil.getValue(this);
  }

  @Override
  public String getName() {
    return SimplePsiImplUtil.getName(this);
  }

  @Override
  public PsiElement setName(@NotNull String newName) {
    return SimplePsiImplUtil.setName(this, newName);
  }

  @Override
  public PsiElement getNameIdentifier() {
    return SimplePsiImplUtil.getNameIdentifier(this);
  }

  @Override
  public ItemPresentation getPresentation() {
    return SimplePsiImplUtil.getPresentation(this);
  }

}

```

# simple_language_plugin/src/main/gen/org/intellij/sdk/language/psi/SimpleProperty.java
```java
// This is a generated file. Not intended for manual editing.
package org.intellij.sdk.language.psi;

import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.PsiElement;
import org.jetbrains.annotations.NotNull;

public interface SimpleProperty extends SimpleNamedElement {

  String getKey();

  String getValue();

  String getName();

  PsiElement setName(@NotNull String newName);

  PsiElement getNameIdentifier();

  ItemPresentation getPresentation();

}

```

# simple_language_plugin/src/main/gen/org/intellij/sdk/language/psi/SimpleVisitor.java
```java
// This is a generated file. Not intended for manual editing.
package org.intellij.sdk.language.psi;

import org.jetbrains.annotations.*;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.PsiElement;

public class SimpleVisitor extends PsiElementVisitor {

  public void visitProperty(@NotNull SimpleProperty o) {
    visitNamedElement(o);
  }

  public void visitNamedElement(@NotNull SimpleNamedElement o) {
    visitPsiElement(o);
  }

  public void visitPsiElement(@NotNull PsiElement o) {
    visitElement(o);
  }

}

```

# simple_language_plugin/src/main/gen/org/intellij/sdk/language/psi/SimpleTypes.java
```java
// This is a generated file. Not intended for manual editing.
package org.intellij.sdk.language.psi;

import com.intellij.psi.tree.IElementType;
import com.intellij.psi.PsiElement;
import com.intellij.lang.ASTNode;
import org.intellij.sdk.language.psi.impl.*;

public interface SimpleTypes {

  IElementType PROPERTY = new SimpleElementType("PROPERTY");

  IElementType COMMENT = new SimpleTokenType("COMMENT");
  IElementType CRLF = new SimpleTokenType("CRLF");
  IElementType KEY = new SimpleTokenType("KEY");
  IElementType SEPARATOR = new SimpleTokenType("SEPARATOR");
  IElementType VALUE = new SimpleTokenType("VALUE");

  class Factory {
    public static PsiElement createElement(ASTNode node) {
      IElementType type = node.getElementType();
      if (type == PROPERTY) {
        return new SimplePropertyImpl(node);
      }
      throw new AssertionError("Unknown element type: " + type);
    }
  }
}

```

# simple_language_plugin/src/main/gen/org/intellij/sdk/language/SimpleLexer.java
```java
// Copyright 2000-2024 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.
// Generated by JFlex 1.9.1 http://jflex.de/  (tweaked for IntelliJ platform)
// source: Simple.flex

package org.intellij.sdk.language;

import com.intellij.lexer.FlexLexer;
import com.intellij.psi.tree.IElementType;
import org.intellij.sdk.language.psi.SimpleTypes;
import com.intellij.psi.TokenType;


class SimpleLexer implements FlexLexer {

  /** This character denotes the end of file */
  public static final int YYEOF = -1;

  /** initial size of the lookahead buffer */
  private static final int ZZ_BUFFERSIZE = 16384;

  /** lexical states */
  public static final int YYINITIAL = 0;
  public static final int WAITING_VALUE = 2;

  /**
   * ZZ_LEXSTATE[l] is the state in the DFA for the lexical state l
   * ZZ_LEXSTATE[l+1] is the state in the DFA for the lexical state l
   *                  at the beginning of a line
   * l is of the form l = 2*k, k a non negative integer
   */
  private static final int ZZ_LEXSTATE[] = {
     0,  0,  1, 1
  };

  /**
   * Top-level table for translating characters to character classes
   */
  private static final int [] ZZ_CMAP_TOP = zzUnpackcmap_top();

  private static final String ZZ_CMAP_TOP_PACKED_0 =
    "\1\0\37\u0100\1\u0200\267\u0100\10\u0300\u1020\u0100";

  private static int [] zzUnpackcmap_top() {
    int [] result = new int[4352];
    int offset = 0;
    offset = zzUnpackcmap_top(ZZ_CMAP_TOP_PACKED_0, offset, result);
    return result;
  }

  private static int zzUnpackcmap_top(String packed, int offset, int [] result) {
    int i = 0;       /* index in packed string  */
    int j = offset;  /* index in unpacked array */
    int l = packed.length();
    while (i < l) {
      int count = packed.charAt(i++);
      int value = packed.charAt(i++);
      do result[j++] = value; while (--count > 0);
    }
    return j;
  }


  /**
   * Second-level tables for translating characters to character classes
   */
  private static final int [] ZZ_CMAP_BLOCKS = zzUnpackcmap_blocks();

  private static final String ZZ_CMAP_BLOCKS_PACKED_0 =
    "\11\0\1\1\1\2\1\3\1\4\1\5\22\0\1\6"+
    "\1\7\1\0\1\7\26\0\1\10\2\0\1\10\36\0"+
    "\1\11\50\0\1\3\u01a2\0\2\3\326\0\u0100\12";

  private static int [] zzUnpackcmap_blocks() {
    int [] result = new int[1024];
    int offset = 0;
    offset = zzUnpackcmap_blocks(ZZ_CMAP_BLOCKS_PACKED_0, offset, result);
    return result;
  }

  private static int zzUnpackcmap_blocks(String packed, int offset, int [] result) {
    int i = 0;       /* index in packed string  */
    int j = offset;  /* index in unpacked array */
    int l = packed.length();
    while (i < l) {
      int count = packed.charAt(i++);
      int value = packed.charAt(i++);
      do result[j++] = value; while (--count > 0);
    }
    return j;
  }

  /**
   * Translates DFA states to action switch labels.
   */
  private static final int [] ZZ_ACTION = zzUnpackAction();

  private static final String ZZ_ACTION_PACKED_0 =
    "\2\0\1\1\1\2\1\1\1\3\1\4\1\5\1\6"+
    "\2\7\1\6\1\7\1\5\1\0\2\3\1\0\1\6"+
    "\1\2\1\6";

  private static int [] zzUnpackAction() {
    int [] result = new int[21];
    int offset = 0;
    offset = zzUnpackAction(ZZ_ACTION_PACKED_0, offset, result);
    return result;
  }

  private static int zzUnpackAction(String packed, int offset, int [] result) {
    int i = 0;       /* index in packed string  */
    int j = offset;  /* index in unpacked array */
    int l = packed.length();
    while (i < l) {
      int count = packed.charAt(i++);
      int value = packed.charAt(i++);
      do result[j++] = value; while (--count > 0);
    }
    return j;
  }


  /**
   * Translates a state to a row index in the transition table
   */
  private static final int [] ZZ_ROWMAP = zzUnpackRowMap();

  private static final String ZZ_ROWMAP_PACKED_0 =
    "\0\0\0\13\0\26\0\41\0\54\0\67\0\102\0\115"+
    "\0\130\0\143\0\41\0\156\0\171\0\204\0\115\0\217"+
    "\0\232\0\204\0\245\0\156\0\260";

  private static int [] zzUnpackRowMap() {
    int [] result = new int[21];
    int offset = 0;
    offset = zzUnpackRowMap(ZZ_ROWMAP_PACKED_0, offset, result);
    return result;
  }

  private static int zzUnpackRowMap(String packed, int offset, int [] result) {
    int i = 0;  /* index in packed string  */
    int j = offset;  /* index in unpacked array */
    int l = packed.length() - 1;
    while (i < l) {
      int high = packed.charAt(i++) << 16;
      result[j++] = high | packed.charAt(i++);
    }
    return j;
  }

  /**
   * The transition table of the DFA
   */
  private static final int [] ZZ_TRANS = zzUnpacktrans();

  private static final String ZZ_TRANS_PACKED_0 =
    "\1\3\2\4\1\5\1\4\1\5\1\4\1\6\1\7"+
    "\1\10\1\3\1\11\1\12\1\13\1\14\1\13\1\14"+
    "\1\15\2\11\1\16\1\11\1\3\2\0\1\3\1\0"+
    "\1\3\1\0\1\3\1\0\1\17\1\3\1\0\6\4"+
    "\4\0\1\3\2\4\1\5\1\4\1\5\1\4\1\3"+
    "\1\0\1\17\1\3\1\6\1\20\1\0\1\6\1\20"+
    "\1\3\1\20\1\6\1\20\1\21\1\6\21\0\1\3"+
    "\4\0\2\11\1\0\1\11\1\0\4\11\1\22\2\11"+
    "\1\12\1\15\1\23\1\15\1\23\1\12\2\11\1\22"+
    "\2\11\1\24\1\4\1\24\1\4\2\24\2\11\1\22"+
    "\1\11\1\0\2\15\1\4\1\15\1\4\1\15\4\0"+
    "\5\11\1\25\4\11\1\0\2\20\1\0\2\20\1\0"+
    "\7\20\1\0\2\20\1\0\1\6\4\20\1\11\1\23"+
    "\1\4\1\23\1\4\2\23\2\11\1\22\5\11\1\0"+
    "\4\11\1\22\1\11";

  private static int [] zzUnpacktrans() {
    int [] result = new int[187];
    int offset = 0;
    offset = zzUnpacktrans(ZZ_TRANS_PACKED_0, offset, result);
    return result;
  }

  private static int zzUnpacktrans(String packed, int offset, int [] result) {
    int i = 0;       /* index in packed string  */
    int j = offset;  /* index in unpacked array */
    int l = packed.length();
    while (i < l) {
      int count = packed.charAt(i++);
      int value = packed.charAt(i++);
      value--;
      do result[j++] = value; while (--count > 0);
    }
    return j;
  }


  /* error codes */
  private static final int ZZ_UNKNOWN_ERROR = 0;
  private static final int ZZ_NO_MATCH = 1;
  private static final int ZZ_PUSHBACK_2BIG = 2;

  /* error messages for the codes above */
  private static final String[] ZZ_ERROR_MSG = {
    "Unknown internal scanner error",
    "Error: could not match input",
    "Error: pushback value was too large"
  };

  /**
   * ZZ_ATTRIBUTE[aState] contains the attributes of state {@code aState}
   */
  private static final int [] ZZ_ATTRIBUTE = zzUnpackAttribute();

  private static final String ZZ_ATTRIBUTE_PACKED_0 =
    "\2\0\4\1\1\11\7\1\1\0\2\1\1\0\3\1";

  private static int [] zzUnpackAttribute() {
    int [] result = new int[21];
    int offset = 0;
    offset = zzUnpackAttribute(ZZ_ATTRIBUTE_PACKED_0, offset, result);
    return result;
  }

  private static int zzUnpackAttribute(String packed, int offset, int [] result) {
    int i = 0;       /* index in packed string  */
    int j = offset;  /* index in unpacked array */
    int l = packed.length();
    while (i < l) {
      int count = packed.charAt(i++);
      int value = packed.charAt(i++);
      do result[j++] = value; while (--count > 0);
    }
    return j;
  }

  /** the input device */
  private java.io.Reader zzReader;

  /** the current state of the DFA */
  private int zzState;

  /** the current lexical state */
  private int zzLexicalState = YYINITIAL;

  /** this buffer contains the current text to be matched and is
      the source of the yytext() string */
  private CharSequence zzBuffer = "";

  /** the textposition at the last accepting state */
  private int zzMarkedPos;

  /** the current text position in the buffer */
  private int zzCurrentPos;

  /** startRead marks the beginning of the yytext() string in the buffer */
  private int zzStartRead;

  /** endRead marks the last character in the buffer, that has been read
      from input */
  private int zzEndRead;

  /** zzAtEOF == true <=> the scanner is at the EOF */
  private boolean zzAtEOF;

  /** Number of newlines encountered up to the start of the matched text. */
  @SuppressWarnings("unused")
  private int yyline;

  /** Number of characters from the last newline up to the start of the matched text. */
  @SuppressWarnings("unused")
  protected int yycolumn;

  /** Number of characters up to the start of the matched text. */
  @SuppressWarnings("unused")
  private long yychar;

  /** Whether the scanner is currently at the beginning of a line. */
  @SuppressWarnings("unused")
  private boolean zzAtBOL = true;

  /** Whether the user-EOF-code has already been executed. */
  private boolean zzEOFDone;


  /**
   * Creates a new scanner
   *
   * @param   in  the java.io.Reader to read input from.
   */
  SimpleLexer(java.io.Reader in) {
    this.zzReader = in;
  }


  /** Returns the maximum size of the scanner buffer, which limits the size of tokens. */
  private int zzMaxBufferLen() {
    return Integer.MAX_VALUE;
  }

  /**  Whether the scanner buffer can grow to accommodate a larger token. */
  private boolean zzCanGrow() {
    return true;
  }

  /**
   * Translates raw input code points to DFA table row
   */
  private static int zzCMap(int input) {
    int offset = input & 255;
    return offset == input ? ZZ_CMAP_BLOCKS[offset] : ZZ_CMAP_BLOCKS[ZZ_CMAP_TOP[input >> 8] | offset];
  }

  public final int getTokenStart() {
    return zzStartRead;
  }

  public final int getTokenEnd() {
    return getTokenStart() + yylength();
  }

  public void reset(CharSequence buffer, int start, int end, int initialState) {
    zzBuffer = buffer;
    zzCurrentPos = zzMarkedPos = zzStartRead = start;
    zzAtEOF  = false;
    zzAtBOL = true;
    zzEndRead = end;
    yybegin(initialState);
  }

  /**
   * Refills the input buffer.
   *
   * @return      {@code false}, iff there was new input.
   *
   * @exception   java.io.IOException  if any I/O-Error occurs
   */
  private boolean zzRefill() throws java.io.IOException {
    return true;
  }


  /**
   * Returns the current lexical state.
   */
  public final int yystate() {
    return zzLexicalState;
  }


  /**
   * Enters a new lexical state
   *
   * @param newState the new lexical state
   */
  public final void yybegin(int newState) {
    zzLexicalState = newState;
  }


  /**
   * Returns the text matched by the current regular expression.
   */
  public final CharSequence yytext() {
    return zzBuffer.subSequence(zzStartRead, zzMarkedPos);
  }


  /**
   * Returns the character at position {@code pos} from the
   * matched text.
   *
   * It is equivalent to yytext().charAt(pos), but faster
   *
   * @param pos the position of the character to fetch.
   *            A value from 0 to yylength()-1.
   *
   * @return the character at position pos
   */
  public final char yycharat(int pos) {
    return zzBuffer.charAt(zzStartRead+pos);
  }


  /**
   * Returns the length of the matched text region.
   */
  public final int yylength() {
    return zzMarkedPos-zzStartRead;
  }


  /**
   * Reports an error that occurred while scanning.
   *
   * In a wellformed scanner (no or only correct usage of
   * yypushback(int) and a match-all fallback rule) this method
   * will only be called with things that "Can't Possibly Happen".
   * If this method is called, something is seriously wrong
   * (e.g. a JFlex bug producing a faulty scanner etc.).
   *
   * Usual syntax/scanner level error handling should be done
   * in error fallback rules.
   *
   * @param   errorCode  the code of the errormessage to display
   */
  private void zzScanError(int errorCode) {
    String message;
    try {
      message = ZZ_ERROR_MSG[errorCode];
    }
    catch (ArrayIndexOutOfBoundsException e) {
      message = ZZ_ERROR_MSG[ZZ_UNKNOWN_ERROR];
    }

    throw new Error(message);
  }


  /**
   * Pushes the specified amount of characters back into the input stream.
   *
   * They will be read again by then next call of the scanning method
   *
   * @param number  the number of characters to be read again.
   *                This number must not be greater than yylength()!
   */
  public void yypushback(int number)  {
    if ( number > yylength() )
      zzScanError(ZZ_PUSHBACK_2BIG);

    zzMarkedPos -= number;
  }


  /**
   * Contains user EOF-code, which will be executed exactly once,
   * when the end of file is reached
   */
  private void zzDoEOF() {
    if (!zzEOFDone) {
      zzEOFDone = true;

    }
  }


  /**
   * Resumes scanning until the next regular expression is matched,
   * the end of input is encountered or an I/O-Error occurs.
   *
   * @return      the next token
   * @exception   java.io.IOException  if any I/O-Error occurs
   */
  public IElementType advance() throws java.io.IOException
  {
    int zzInput;
    int zzAction;

    // cached fields:
    int zzCurrentPosL;
    int zzMarkedPosL;
    int zzEndReadL = zzEndRead;
    CharSequence zzBufferL = zzBuffer;

    int [] zzTransL = ZZ_TRANS;
    int [] zzRowMapL = ZZ_ROWMAP;
    int [] zzAttrL = ZZ_ATTRIBUTE;

    while (true) {
      zzMarkedPosL = zzMarkedPos;

      zzAction = -1;

      zzCurrentPosL = zzCurrentPos = zzStartRead = zzMarkedPosL;

      zzState = ZZ_LEXSTATE[zzLexicalState];

      // set up zzAction for empty match case:
      int zzAttributes = zzAttrL[zzState];
      if ( (zzAttributes & 1) == 1 ) {
        zzAction = zzState;
      }


      zzForAction: {
        while (true) {

          if (zzCurrentPosL < zzEndReadL) {
            zzInput = Character.codePointAt(zzBufferL, zzCurrentPosL);
            zzCurrentPosL += Character.charCount(zzInput);
          }
          else if (zzAtEOF) {
            zzInput = YYEOF;
            break zzForAction;
          }
          else {
            // store back cached positions
            zzCurrentPos  = zzCurrentPosL;
            zzMarkedPos   = zzMarkedPosL;
            boolean eof = zzRefill();
            // get translated positions and possibly new buffer
            zzCurrentPosL  = zzCurrentPos;
            zzMarkedPosL   = zzMarkedPos;
            zzBufferL      = zzBuffer;
            zzEndReadL     = zzEndRead;
            if (eof) {
              zzInput = YYEOF;
              break zzForAction;
            }
            else {
              zzInput = Character.codePointAt(zzBufferL, zzCurrentPosL);
              zzCurrentPosL += Character.charCount(zzInput);
            }
          }
          int zzNext = zzTransL[ zzRowMapL[zzState] + zzCMap(zzInput) ];
          if (zzNext == -1) break zzForAction;
          zzState = zzNext;

          zzAttributes = zzAttrL[zzState];
          if ( (zzAttributes & 1) == 1 ) {
            zzAction = zzState;
            zzMarkedPosL = zzCurrentPosL;
            if ( (zzAttributes & 8) == 8 ) break zzForAction;
          }

        }
      }

      // store back cached position
      zzMarkedPos = zzMarkedPosL;

      if (zzInput == YYEOF && zzStartRead == zzCurrentPos) {
        zzAtEOF = true;
            zzDoEOF();
        return null;
      }
      else {
        switch (zzAction < 0 ? zzAction : ZZ_ACTION[zzAction]) {
          case 1:
            { yybegin(YYINITIAL); return SimpleTypes.KEY;
            }
          // fall through
          case 8: break;
          case 2:
            { yybegin(YYINITIAL); return TokenType.WHITE_SPACE;
            }
          // fall through
          case 9: break;
          case 3:
            { yybegin(YYINITIAL); return SimpleTypes.COMMENT;
            }
          // fall through
          case 10: break;
          case 4:
            { yybegin(WAITING_VALUE); return SimpleTypes.SEPARATOR;
            }
          // fall through
          case 11: break;
          case 5:
            { return TokenType.BAD_CHARACTER;
            }
          // fall through
          case 12: break;
          case 6:
            { yybegin(YYINITIAL); return SimpleTypes.VALUE;
            }
          // fall through
          case 13: break;
          case 7:
            { yybegin(WAITING_VALUE); return TokenType.WHITE_SPACE;
            }
          // fall through
          case 14: break;
          default:
            zzScanError(ZZ_NO_MATCH);
          }
      }
    }
  }


}

```

# product_specific/pycharm_basics/README.md
# PyCharm Sample [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [PyCharm Plugin Development in IntelliJ SDK Docs][docs:pycharm]*

## Quickstart

PyCharm Sample is a plugin that depends on the PyCharm IDE having the proper dependencies specified in the Gradle configuration file.
The implementation utilizes a simple action added to the *MainMenu* group displaying a message dialog after invoking.

### Actions

| ID                                           | Implementation                              | Base Action Class |
|----------------------------------------------|---------------------------------------------|-------------------|
| `org.intellij.sdk.pycharm.PopupDialogAction` | [PopupDialogAction][file:PopupDialogAction] | `AnAction`        |

*Reference: [Action System in IntelliJ SDK Docs][docs:actions]*

[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:actions]: https://plugins.jetbrains.com/docs/intellij/basic-action-system.html
[docs:pycharm]: https://plugins.jetbrains.com/docs/intellij/pycharm.html

[file:PopupDialogAction]: ./src/main/java/org/intellij/sdk/pycharm/PopupDialogAction.java


# product_specific/pycharm_basics/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "com.intellij.sdk"
version = "0.1.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
  type.set("PY")
  plugins.set(listOf("Pythonid"))
  downloadSources.set(false)
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# product_specific/pycharm_basics/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "pycharm_basics"

```

# product_specific/pycharm_basics/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.pycharm</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: PyCharm Sample</name>

  <!-- Requires the python plugin to run -->
  <depends>com.intellij.modules.python</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates how to configure a plugin project for a PyCharm plugin.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <b>0.1.0</b> First release v2019.1 IntelliJ Platform / PyCharm<br>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <actions>
    <!-- Define a new menu group as a last entry in the main menu -->
    <group id="org.intellij.sdk.pycharm.NewGroupedActions" text="SDK: Plugin" popup="true">
      <add-to-group group-id="MainMenu" anchor="last"/>
      <!-- Add a single action to the new group -->
      <action id="org.intellij.sdk.pycharm.PopupDialogAction" class="org.intellij.sdk.pycharm.PopupDialogAction"
              text="Pop a Dialog" description="SDK PyCharm basics example" icon="SdkIcons.Sdk_default_icon">
      </action>
    </group>
  </actions>

</idea-plugin>

```

# product_specific/pycharm_basics/src/main/java/org/intellij/sdk/pycharm/PopupDialogAction.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.pycharm;

import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.Messages;
import org.jetbrains.annotations.NotNull;

/**
 * Action class to demonstrate how to interact with the IntelliJ Platform.
 * The only action this class performs is to provide the user with a popup dialog as feedback.
 * Typically this class is instantiated by the IntelliJ Platform framework based on declarations
 * in the plugin.xml file. But when added at runtime this class is instantiated by an action group.
 */
public class PopupDialogAction extends AnAction {

  /**
   * Gives the user feedback when the dynamic action menu is chosen.
   * Pops a simple message dialog. See the psi_demo plugin for an example of how to use AnActionEvent to access data.
   *
   * @param event Event received when the associated menu item is chosen.
   */
  @Override
  public void actionPerformed(@NotNull AnActionEvent event) {
    Project project = event.getProject();
    Messages.showMessageDialog(project,
        "Popup dialog action",
        "Greetings from PyCharm Basics Plugin",
        Messages.getInformationIcon());
  }

  /**
   * Determines whether this menu item is available for the current context.
   * Requires a project to be open.
   *
   * @param e Event received when the associated group-id menu is chosen.
   */
  @Override
  public void update(AnActionEvent e) {
    // Set the availability based on whether a project is open
    Project project = e.getProject();
    e.getPresentation().setEnabledAndVisible(project != null);
  }

}

```

# product_specific/pycharm_basics/src/main/java/icons/SdkIcons.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package icons;

import com.intellij.openapi.util.IconLoader;

import javax.swing.*;

public class SdkIcons {

  public static final Icon Sdk_default_icon = IconLoader.getIcon("/icons/sdk_16.svg", SdkIcons.class);

}

```

# product_specific/README.md
## Product Specific Code Samples

Please note, all samples in this folder must be imported into Gradle explicitly as they're not included in the default Gradle composite build.


# theme_basics/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.themeBasics</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Theme Basics</name>

  <!-- The version of this plugin -->
  <version>0.1</version>

  <!-- Compatible with the following versions of IntelliJ Platform: version 2022.1 and newer. -->
  <idea-version since-build="221"/>

  <!-- Indicate this plugin can be loaded in all IntelliJ Platform-based products. -->
  <depends>com.intellij.modules.platform</depends>

  <description>
    <![CDATA[
      IntelliJ Platform SDK code sample to illustrate creating <em>themes</em>.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>0.1</b> Initial release. Basic theme functionality.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <themeProvider id="eb9b7461-397b-4b98-a422-224fc0a74564" path="/theme_basics.theme.json"/>
  </extensions>

</idea-plugin>

```

# theme_basics/resources/Lightning.xml
```xml
<!-- Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->

<scheme name="Lightning" version="142" parent_scheme="Default">
  <metaInfo>
    <property name="created">2019-01-22T02:54:51</property>
    <property name="ide">idea</property>
    <property name="ideVersion">2019.1.0.0</property>
    <property name="modified">2019-01-22T02:55:20</property>
    <property name="originalScheme">Lightning</property>
  </metaInfo>
  <colors>
    <option name="CARET_ROW_COLOR" value="e8e3cf" />
  </colors>
  <attributes>
    <option name="BAD_CHARACTER">
      <value>
        <option name="FOREGROUND" value="ff0000" />
      </value>
    </option>
    <option name="CONSTRUCTOR_CALL_ATTRIBUTES">
      <value>
        <option name="FOREGROUND" value="b5" />
      </value>
    </option>
    <option name="DEFAULT_ATTRIBUTE">
      <value>
        <option name="FOREGROUND" value="b2" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="DEFAULT_CLASS_NAME">
      <value>
        <option name="FOREGROUND" value="27c7e" />
      </value>
    </option>
    <option name="DEFAULT_CONSTANT">
      <value>
        <option name="FOREGROUND" value="d101d9" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <option name="DEFAULT_DOC_MARKUP">
      <value>
        <option name="BACKGROUND" value="e6eae8" />
      </value>
    </option>
    <option name="DEFAULT_ENTITY">
      <value>
        <option name="FOREGROUND" value="b2" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="DEFAULT_FUNCTION_CALL">
      <value>
        <option name="FOREGROUND" value="2686a" />
      </value>
    </option>
    <option name="DEFAULT_FUNCTION_DECLARATION">
      <value>
        <option name="FOREGROUND" value="27c7e" />
      </value>
    </option>
    <option name="DEFAULT_GLOBAL_VARIABLE">
      <value>
        <option name="FOREGROUND" value="3c90" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <option name="DEFAULT_INSTANCE_FIELD">
      <value>
        <option name="FOREGROUND" value="2686a" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="DEFAULT_INSTANCE_METHOD">
      <value>
        <option name="FOREGROUND" value="2686a" />
      </value>
    </option>
    <option name="DEFAULT_INTERFACE_NAME">
      <value>
        <option name="FOREGROUND" value="27c7e" />
      </value>
    </option>
    <option name="DEFAULT_INVALID_STRING_ESCAPE">
      <value>
        <option name="FOREGROUND" value="ff0000" />
      </value>
    </option>
    <option name="DEFAULT_KEYWORD">
      <value>
        <option name="FOREGROUND" value="3504a8" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="DEFAULT_LOCAL_VARIABLE">
      <value>
        <option name="FOREGROUND" value="69ff" />
      </value>
    </option>
    <option name="DEFAULT_METADATA">
      <value>
        <option name="FOREGROUND" value="a09d6b" />
        <option name="BACKGROUND" value="ffffff" />
      </value>
    </option>
    <option name="DEFAULT_NUMBER">
      <value>
        <option name="FOREGROUND" value="46d8" />
      </value>
    </option>
    <option name="DEFAULT_PARAMETER">
      <value>
        <option name="FOREGROUND" value="6c0063" />
      </value>
    </option>
    <option name="DEFAULT_STATIC_FIELD">
      <value>
        <option name="FOREGROUND" value="2686a" />
        <option name="FONT_TYPE" value="3" />
      </value>
    </option>
    <option name="DEFAULT_STATIC_METHOD">
      <value>
        <option name="FOREGROUND" value="2686a" />
        <option name="FONT_TYPE" value="2" />
        <option name="EFFECT_TYPE" value="1" />
      </value>
    </option>
    <option name="DEFAULT_STRING">
      <value>
        <option name="FOREGROUND" value="1a114" />
      </value>
    </option>
    <option name="IMPLICIT_ANONYMOUS_CLASS_PARAMETER_ATTRIBUTES">
      <value>
        <option name="FOREGROUND" value="27d7f" />
      </value>
    </option>
    <option name="INHERITED_METHOD_ATTRIBUTES">
      <value>
        <option name="FOREGROUND" value="b5" />
        <option name="EFFECT_COLOR" value="b5" />
        <option name="EFFECT_TYPE" value="1" />
      </value>
    </option>
    <option name="INSTANCE_FINAL_FIELD_ATTRIBUTES">
      <value>
        <option name="FOREGROUND" value="8f0197" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="METHOD_CALL_ATTRIBUTES">
      <value>
        <option name="FOREGROUND" value="b5" />
      </value>
    </option>
    <option name="METHOD_DECLARATION_ATTRIBUTES">
      <value>
        <option name="FOREGROUND" value="b5" />
        <option name="FONT_TYPE" value="1" />
      </value>
    </option>
    <option name="NOT_USED_ELEMENT_ATTRIBUTES">
      <value>
        <option name="FOREGROUND" value="808080" />
        <option name="BACKGROUND" value="ffffff" />
      </value>
    </option>
    <option name="STATIC_FINAL_FIELD_ATTRIBUTES">
      <value>
        <option name="FOREGROUND" value="d101d9" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <option name="STATIC_FINAL_FIELD_IMPORTED_ATTRIBUTES">
      <value>
        <option name="FOREGROUND" value="d101d9" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <option name="TODO_DEFAULT_ATTRIBUTES">
      <value>
        <option name="FOREGROUND" value="ba7480" />
        <option name="FONT_TYPE" value="2" />
      </value>
    </option>
    <option name="UNMATCHED_BRACE_ATTRIBUTES">
      <value>
        <option name="BACKGROUND" value="ff8a8a" />
      </value>
    </option>
    <option name="XML_ATTRIBUTE_VALUE">
      <value>
        <option name="FOREGROUND" value="17913" />
      </value>
    </option>
  </attributes>
</scheme>

```

# theme_basics/README.md
# Theme Basics [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Creating Custom Themes in IntelliJ SDK Docs][docs:themes]*

## Quickstart

Custom themes are available beginning in version 2019.1.

Creating a custom theme is a process of choosing a base IDE Theme (Light or Darcula) then changing aspects of the base Theme definition.
Custom themes can:
- substitute icons,
- change the colors of icons and UI controls,
- alter the borders and insets of UI controls,
- provide custom editor schemes,
- add background images.

## Structure

Theme Basics plugin depends on the [IntelliJ Platform SDK][docs] and [DevKit][docs:devkit] as a build system.

The main plugin definition file is stored in the [plugin.xml][file:plugin.xml] file, which is created according to the [Plugin Configuration File documentation][docs:plugin.xml].
It describes definitions of the actions, extensions, or listeners provided by the plugin.

### Extension Points

| Name                         | Implementation                                          | Extension Point Class |
|------------------------------|---------------------------------------------------------|-----------------------|
| `com.intellij.themeProvider` | [theme_basics.theme.json][file:theme_basics.theme.json] |                       |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:themes]: https://plugins.jetbrains.com/docs/intellij/themes-getting-started.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html
[docs:devkit]: https://plugins.jetbrains.com/docs/intellij/developing-themes.html
[docs:plugin.xml]: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html

[file:plugin.xml]: ./resources/META-INF/plugin.xml
[file:theme_basics.theme.json]: ./resources/theme_basics.theme.json

## Troubleshooting

To run the `theme_basics` plugin make sure that module SDK is correctly set up and points to IntelliJ Platform Plugin SDK, e.g. `IntelliJ IDEA IC-<version>`. To check this, go to **File | Project Structure | Project Settings | Modules | theme_basics** and select **Dependencies** tab.

If the required SDK doesn't exist, it can be added in **File | Project Structure | Platform Settings | SDKs** by clicking the plus button and selecting **Add IntelliJ Platform Plugin SDK...** item.


# framework_basics/README.md
# Framework Sample Project [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Supporting Frameworks in IntelliJ SDK Docs][docs:supporting_frameworks]*

## Quickstart

Framework Sample Project provides a [DemoFramework][file:DemoFramework], which allows embedding framework support within the Project Wizard.
This sample implementation adds a new *SDK Demo Framework* support in the Java type project.

### Extension Points

| Name                          | Implementation                      | Extension Point Class |
|-------------------------------|-------------------------------------|-----------------------|
| `com.intellij.framework.type` | [DemoFramework][file:DemoFramework] | `FrameworkTypeEx`     |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:supporting_frameworks]: https://plugins.jetbrains.com/docs/intellij/framework.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:DemoFramework]: ./src/main/java/org/intellij/sdk/framework/DemoFramework.java


# framework_basics/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
  plugins.set(listOf("com.intellij.java"))
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# framework_basics/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "framework_basics"

```

# framework_basics/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# framework_basics/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.framework</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Framework Sample</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.platform</depends>
  <depends>com.intellij.java</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates basic Framework support. <br>Adds <i>SDK Demo Framework</i> to
      <b>File | New | Project | IntelliJ Platform Plugin</b>
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin, rename to framework_basics, change plugin ID</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>


  <extensions defaultExtensionNs="com.intellij">
    <framework.type implementation="org.intellij.sdk.framework.DemoFramework"/>
  </extensions>

</idea-plugin>

```

# framework_basics/src/main/java/org/intellij/sdk/framework/DemoFramework.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package org.intellij.sdk.framework;

import com.intellij.framework.FrameworkTypeEx;
import com.intellij.framework.addSupport.FrameworkSupportInModuleConfigurable;
import com.intellij.framework.addSupport.FrameworkSupportInModuleProvider;
import com.intellij.ide.util.frameworkSupport.FrameworkSupportModel;
import com.intellij.openapi.module.Module;
import com.intellij.openapi.module.ModuleType;
import com.intellij.openapi.roots.ModifiableModelsProvider;
import com.intellij.openapi.roots.ModifiableRootModel;
import icons.SdkIcons;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

final class DemoFramework extends FrameworkTypeEx {

  public static final String FRAMEWORK_ID = "org.intellij.sdk.framework.DemoFramework";

  DemoFramework() {
    super(FRAMEWORK_ID);
  }

  @NotNull
  @Override
  public FrameworkSupportInModuleProvider createProvider() {
    return new FrameworkSupportInModuleProvider() {
      @NotNull
      @Override
      public FrameworkTypeEx getFrameworkType() {
        return DemoFramework.this;
      }

      @NotNull
      @Override
      public FrameworkSupportInModuleConfigurable createConfigurable(@NotNull FrameworkSupportModel model) {
        return new FrameworkSupportInModuleConfigurable() {

          @Override
          public JComponent createComponent() {
            return new JCheckBox("SDK Extra Option");
          }

          @Override
          public void addSupport(@NotNull Module module,
                                 @NotNull ModifiableRootModel model,
                                 @NotNull ModifiableModelsProvider provider) {
            // This is the place to set up a library, generate a specific file, etc
            // and actually add framework support to a module.
          }
        };
      }

      @Override
      public boolean isEnabledForModuleType(@NotNull ModuleType type) {
        return true;
      }
    };
  }

  @NotNull
  @Override
  public String getPresentableName() {
    return "SDK Demo Framework";
  }

  @NotNull
  @Override
  public Icon getIcon() {
    return SdkIcons.Sdk_default_icon;
  }

}

```

# framework_basics/src/main/java/icons/SdkIcons.java
```java
// Copyright 2000-2022 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file.

package icons;

import com.intellij.openapi.util.IconLoader;

import javax.swing.*;

public class SdkIcons {

  public static final Icon Sdk_default_icon = IconLoader.getIcon("/icons/sdk_16.svg", SdkIcons.class);

}

```

# conditional_operator_intention/README.md
# Conditional Operator Converter [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Code Intentions in IntelliJ SDK Docs][docs:conditional_operator_intention]*

## Quickstart

Conditional Operator Converter provides an intention for converting the *ternary operator* into the *if* statement, i.e.:

```java
public class X {
  void f(boolean isMale) {
    String title = isMale ? "Mr." : "Ms.";
    System.out.println("title = " + title);
 }
}
```

will become:

```java
public class X {
  void f(boolean isMale) {
    String title;
    if (isMale) {
      title = "Mr.";
    } else {
      title = "Ms.";
    }
    System.out.println("title = " + title);
  }
}
```

To invoke the intention action, it is necessary to place the caret on the `?` character of the ternary operator.
The converter in the `isAvailable` method, has defined the token check to match `JavaTokenType.QUEST`, which is `?` character.

### Extension Points

| Name                           | Implementation                                                    | Extension Point Class           |
|--------------------------------|-------------------------------------------------------------------|---------------------------------|
| `com.intellij.intentionAction` | [ConditionalOperatorConverter][file:ConditionalOperatorConverter] | `PsiElementBaseIntentionAction` |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:conditional_operator_intention]: https://plugins.jetbrains.com/docs/intellij/code-intentions.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:ConditionalOperatorConverter]: ./src/main/java/org/intellij/sdk/intention/ConditionalOperatorConverter.java


# conditional_operator_intention/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

dependencies {
  testImplementation("junit:junit:4.13.2")
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
  plugins.set(listOf("com.intellij.java"))
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# conditional_operator_intention/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "conditional_operator_intention"

```

# conditional_operator_intention/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# conditional_operator_intention/src/test/testData/before.template.java
```java
public class X {
    void f(boolean isMale) {
        String title = isMale <caret>? "Mr." : "Ms.";
        System.out.println("title = " + title);
    }
}
```

# conditional_operator_intention/src/test/testData/before.template.after.java
```java
public class X {
    void f(boolean isMale) {
        String title;
        if (isMale) {
            title = "Mr.";
        } else {
            title = "Ms.";
        }
        System.out.println("title = " + title);
    }
}
```

# conditional_operator_intention/src/test/java/org/intellij/sdk/intention/ConditionalOperatorConverterTest.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.
package org.intellij.sdk.intention;

import com.intellij.codeInsight.intention.IntentionAction;
import com.intellij.testFramework.fixtures.LightJavaCodeInsightFixtureTestCase;
import org.junit.Assert;

public class ConditionalOperatorConverterTest extends LightJavaCodeInsightFixtureTestCase {

  /**
   * Defines path to files used for running tests.
   *
   * @return The path from this module's root directory ({@code $MODULE_WORKING_DIR$}) to the
   * directory containing files for these tests.
   */
  @Override
  protected String getTestDataPath() {
    return "src/test/testData";
  }

  protected void doTest(String testName, String hint) {
    myFixture.configureByFile(testName + ".java");
    final IntentionAction action = myFixture.findSingleIntention(hint);
    Assert.assertNotNull(action);
    myFixture.launchAction(action);
    myFixture.checkResultByFile(testName + ".after.java");
  }

  public void testIntention() {
    doTest("before.template", "SDK: Convert ternary operator to if statement");
  }

}

```

# conditional_operator_intention/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.intention</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Conditional Operator Converter</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.java</depends>
  <depends>com.intellij.modules.platform</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Intention action that suggests converting a ternary operator into an 'if' block.<br>
      Adds entry to <b>Settings | Editor | Intentions | SDK Intentions<b>.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle.</li>
        <li><b>1.4.0</b> Refactor resources, general cleanup.</li>
        <li><b>1.3.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <intentionAction>
      <language>JAVA</language> <!-- available in 2022.3 and later -->
      <className>org.intellij.sdk.intention.ConditionalOperatorConverter</className>
      <category>SDK intentions</category>
    </intentionAction>
  </extensions>

</idea-plugin>

```

# conditional_operator_intention/src/main/java/org/intellij/sdk/intention/ConditionalOperatorConverter.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.
package org.intellij.sdk.intention;

import com.intellij.codeInsight.intention.IntentionAction;
import com.intellij.codeInsight.intention.PsiElementBaseIntentionAction;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.project.Project;
import com.intellij.psi.*;
import com.intellij.psi.codeStyle.CodeStyleManager;
import com.intellij.psi.util.PsiTreeUtil;
import com.intellij.util.IncorrectOperationException;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * Implements an intention action to replace a ternary statement with if-then-else.
 */
@NonNls
final class ConditionalOperatorConverter extends PsiElementBaseIntentionAction implements IntentionAction {

  /**
   * Checks whether this intention is available at the caret offset in file - the caret must sit just before a "?"
   * character in a ternary statement. If this condition is met, this intention's entry is shown in the available
   * intentions list.
   *
   * <p>Note: this method must do its checks quickly and return.</p>
   *
   * @param project a reference to the Project object being edited.
   * @param editor  a reference to the object editing the project source
   * @param element a reference to the PSI element currently under the caret
   * @return {@code true} if the caret is in a literal string element, so this functionality should be added to the
   * intention menu or {@code false} for all other types of caret positions
   */
  public boolean isAvailable(@NotNull Project project, Editor editor, @Nullable PsiElement element) {
    // Quick sanity check
    if (element == null) {
      return false;
    }

    // Is this a token of type representing a "?" character?
    if (element instanceof PsiJavaToken token) {
      if (token.getTokenType() != JavaTokenType.QUEST) {
        return false;
      }
      // Is this token part of a fully formed conditional, i.e. a ternary?
      if (token.getParent() instanceof PsiConditionalExpression conditionalExpression) {
        // Satisfies all criteria; call back invoke method
        return conditionalExpression.getThenExpression() != null && conditionalExpression.getElseExpression() != null;
      }
      return false;
    }
    return false;
  }

  /**
   * Modifies the PSI to change a ternary expression to an if-then-else statement.
   * If the ternary is part of a declaration, the declaration is separated and moved above the if-then-else statement.
   * Called when user selects this intention action from the available intentions list.
   *
   * @param project a reference to the Project object being edited.
   * @param editor  a reference to the object editing the project source
   * @param element a reference to the PSI element currently under the caret
   * @throws IncorrectOperationException Thrown by underlying (PSI model) write action context
   *                                     when manipulation of the PSI tree fails.
   */
  public void invoke(@NotNull Project project, Editor editor, @NotNull PsiElement element)
      throws IncorrectOperationException {
    // Get the factory for making new PsiElements, and the code style manager to format new statements
    PsiElementFactory factory = JavaPsiFacade.getInstance(project).getElementFactory();
    CodeStyleManager codeStylist = CodeStyleManager.getInstance(project);

    // Get the parent of the "?" element in the ternary statement to find the conditional expression that contains it
    PsiConditionalExpression conditionalExpression =
        PsiTreeUtil.getParentOfType(element, PsiConditionalExpression.class, false);
    if (conditionalExpression == null) {
      return;
    }
    // Verify the conditional expression exists and has two outcomes in the ternary statement.
    PsiExpression thenExpression = conditionalExpression.getThenExpression();
    PsiExpression elseExpression = conditionalExpression.getElseExpression();
    if (thenExpression == null || elseExpression == null) {
      return;
    }

    // Keep searching up the PSI Tree in case the ternary is part of a FOR statement.
    PsiElement originalStatement = PsiTreeUtil.getParentOfType(conditionalExpression, PsiStatement.class, false);
    while (originalStatement instanceof PsiForStatement) {
      originalStatement = PsiTreeUtil.getParentOfType(originalStatement, PsiStatement.class, true);
    }
    if (originalStatement == null) {
      return;
    }

    // If the original statement is a declaration based on a ternary operator,
    // split the declaration and assignment
    if (originalStatement instanceof PsiDeclarationStatement declaration) {
      // Find the local variable within the declaration statement
      PsiElement[] declaredElements = declaration.getDeclaredElements();
      PsiLocalVariable variable = null;
      for (PsiElement declaredElement : declaredElements) {
        if (declaredElement instanceof PsiLocalVariable &&
            PsiTreeUtil.isAncestor(declaredElement, conditionalExpression, true)) {
          variable = (PsiLocalVariable) declaredElement;
          break;
        }
      }
      if (variable == null) {
        return;
      }

      // Ensure that the variable declaration is not combined with other declarations, and add a mark
      variable.normalizeDeclaration();
      Object marker = new Object();
      PsiTreeUtil.mark(conditionalExpression, marker);

      // Create a new expression to declare the local variable
      PsiExpressionStatement statement =
          (PsiExpressionStatement) factory.createStatementFromText(variable.getName() + " = 0;", null);
      statement = (PsiExpressionStatement) codeStylist.reformat(statement);

      // Replace initializer with the ternary expression, making an assignment statement using the ternary
      PsiExpression rExpression = ((PsiAssignmentExpression) statement.getExpression()).getRExpression();
      PsiExpression variableInitializer = variable.getInitializer();
      if (rExpression == null || variableInitializer == null) {
        return;
      }
      rExpression.replace(variableInitializer);

      // Remove the initializer portion of the local variable statement,
      // making it a declaration statement with no initializer
      variableInitializer.delete();

      // Get the grandparent of the local var declaration, and add the new declaration just beneath it
      PsiElement variableParent = variable.getParent();
      originalStatement = variableParent.getParent().addAfter(statement, variableParent);
      conditionalExpression = (PsiConditionalExpression) PsiTreeUtil.releaseMark(originalStatement, marker);
    }
    if (conditionalExpression == null) {
      return;
    }

    // Create an IF statement from a string with placeholder elements.
    // This will replace the ternary statement
    PsiIfStatement newIfStmt = (PsiIfStatement) factory.createStatementFromText("if (true) {a=b;} else {c=d;}", null);
    newIfStmt = (PsiIfStatement) codeStylist.reformat(newIfStmt);

    // Replace the conditional expression with the one from the original ternary expression
    PsiReferenceExpression condition = (PsiReferenceExpression) conditionalExpression.getCondition().copy();
    PsiExpression newIfStmtCondition = newIfStmt.getCondition();
    if (newIfStmtCondition == null) {
      return;
    }
    newIfStmtCondition.replace(condition);

    // Begin building the assignment string for the THEN and ELSE clauses using the
    // parent of the ternary conditional expression
    PsiAssignmentExpression assignmentExpression =
        PsiTreeUtil.getParentOfType(conditionalExpression, PsiAssignmentExpression.class, false);
    if (assignmentExpression == null) {
      return;
    }
    // Get the contents of the assignment expression up to the start of the ternary expression
    String exprFrag = assignmentExpression.getLExpression().getText()
        + assignmentExpression.getOperationSign().getText();

    // Build the THEN statement string for the new IF statement,
    // make a PsiExpressionStatement from the string, and switch the placeholder
    String thenStr = exprFrag + thenExpression.getText() + ";";
    PsiExpressionStatement thenStmt = (PsiExpressionStatement) factory.createStatementFromText(thenStr, null);
    PsiBlockStatement thenBranch = (PsiBlockStatement) newIfStmt.getThenBranch();
    if (thenBranch == null) {
      return;
    }
    thenBranch.getCodeBlock().getStatements()[0].replace(thenStmt);

    // Build the ELSE statement string for the new IF statement,
    // make a PsiExpressionStatement from the string, and switch the placeholder
    String elseStr = exprFrag + elseExpression.getText() + ";";
    PsiExpressionStatement elseStmt = (PsiExpressionStatement) factory.createStatementFromText(elseStr, null);
    PsiBlockStatement elseBranch = (PsiBlockStatement) newIfStmt.getElseBranch();
    if (elseBranch == null) {
      return;
    }
    elseBranch.getCodeBlock().getStatements()[0].replace(elseStmt);

    // Replace the entire original statement with the new IF
    originalStatement.replace(newIfStmt);
  }

  /**
   * If this action is applicable, returns the text to be shown in the list of intention actions available.
   */
  @NotNull
  public String getText() {
    return getFamilyName();
  }

  /**
   * Returns text for name of this family of intentions.
   * It is used to externalize "auto-show" state of intentions.
   * It is also the directory name for the descriptions.
   *
   * @return the intention family name.
   */
  @NotNull
  public String getFamilyName() {
    return "SDK: Convert ternary operator to if statement";
  }

}

```

# tool_window/README.md
# Tool Window Sample [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Tool Windows in IntelliJ SDK Docs][docs:tool_windows]*

## Quickstart

Tool Windows are child windows of the IDE used to display information.
These windows generally have their toolbars (referred to as tool window bars) along the outer edges of the main window containing one or more tool window buttons, which activate panels displayed on the left, bottom, and right sides of the main IDE window.

The current implementation displays a `JPanel` component containing simple icons and information about the actual system date, time, and timezone.
Component is provided by the `CalendarToolWindowFactory.CalendarToolWindowContent` class through the `getContentPanel()` method invoked inside the `CalendarToolWindowFactory` implementation.

### Extension Points

| Name                      | Implementation                                              | Extension Point Class |
|---------------------------|-------------------------------------------------------------|-----------------------|
| `com.intellij.toolWindow` | [CalendarToolWindowFactory][file:CalendarToolWindowFactory] | `ToolWindowFactory`   |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:tool_windows]: https://plugins.jetbrains.com/docs/intellij/tool-windows.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:CalendarToolWindowFactory]: ./src/main/java/org/intellij/sdk/toolWindow/CalendarToolWindowFactory.java


# tool_window/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# tool_window/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "tool_window"

```

# tool_window/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# tool_window/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.toolWindow</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Tool Window Sample</name>

  <!-- Indicate this plugin can be loaded in all IntelliJ Platform-based products. -->
  <depends>com.intellij.modules.platform</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      This sample plugin illustrates how to create your custom tool window.<br>
      See the
      <a href="https://plugins.jetbrains.com/docs/intellij/tool-windows.html">Tool Windows</a>
      for more information.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin.</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <toolWindow id="Sample Calendar" secondary="true" icon="AllIcons.Toolwindows.WebToolWindow" anchor="right"
                factoryClass="org.intellij.sdk.toolWindow.CalendarToolWindowFactory"/>
  </extensions>

</idea-plugin>

```

# tool_window/src/main/java/org/intellij/sdk/toolWindow/CalendarToolWindowFactory.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.
package org.intellij.sdk.toolWindow;

import com.intellij.openapi.project.DumbAware;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.wm.ToolWindow;
import com.intellij.openapi.wm.ToolWindowFactory;
import com.intellij.ui.content.Content;
import com.intellij.ui.content.ContentFactory;
import org.apache.commons.lang3.StringUtils;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;
import java.awt.*;
import java.util.Calendar;
import java.util.Objects;

final class CalendarToolWindowFactory implements ToolWindowFactory, DumbAware {

  @Override
  public void createToolWindowContent(@NotNull Project project, @NotNull ToolWindow toolWindow) {
    CalendarToolWindowContent toolWindowContent = new CalendarToolWindowContent(toolWindow);
    Content content = ContentFactory.getInstance().createContent(toolWindowContent.getContentPanel(), "", false);
    toolWindow.getContentManager().addContent(content);
  }

  private static class CalendarToolWindowContent {

    private static final String CALENDAR_ICON_PATH = "/toolWindow/Calendar-icon.png";
    private static final String TIME_ZONE_ICON_PATH = "/toolWindow/Time-zone-icon.png";
    private static final String TIME_ICON_PATH = "/toolWindow/Time-icon.png";

    private final JPanel contentPanel = new JPanel();
    private final JLabel currentDate = new JLabel();
    private final JLabel timeZone = new JLabel();
    private final JLabel currentTime = new JLabel();

    public CalendarToolWindowContent(ToolWindow toolWindow) {
      contentPanel.setLayout(new BorderLayout(0, 20));
      contentPanel.setBorder(BorderFactory.createEmptyBorder(40, 0, 0, 0));
      contentPanel.add(createCalendarPanel(), BorderLayout.PAGE_START);
      contentPanel.add(createControlsPanel(toolWindow), BorderLayout.CENTER);
      updateCurrentDateTime();
    }

    @NotNull
    private JPanel createCalendarPanel() {
      JPanel calendarPanel = new JPanel();
      setIconLabel(currentDate, CALENDAR_ICON_PATH);
      setIconLabel(timeZone, TIME_ZONE_ICON_PATH);
      setIconLabel(currentTime, TIME_ICON_PATH);
      calendarPanel.add(currentDate);
      calendarPanel.add(timeZone);
      calendarPanel.add(currentTime);
      return calendarPanel;
    }

    private void setIconLabel(JLabel label, String imagePath) {
      label.setIcon(new ImageIcon(Objects.requireNonNull(getClass().getResource(imagePath))));
    }

    @NotNull
    private JPanel createControlsPanel(ToolWindow toolWindow) {
      JPanel controlsPanel = new JPanel();
      JButton refreshDateAndTimeButton = new JButton("Refresh");
      refreshDateAndTimeButton.addActionListener(e -> updateCurrentDateTime());
      controlsPanel.add(refreshDateAndTimeButton);
      JButton hideToolWindowButton = new JButton("Hide");
      hideToolWindowButton.addActionListener(e -> toolWindow.hide(null));
      controlsPanel.add(hideToolWindowButton);
      return controlsPanel;
    }

    private void updateCurrentDateTime() {
      Calendar calendar = Calendar.getInstance();
      currentDate.setText(getCurrentDate(calendar));
      timeZone.setText(getTimeZone(calendar));
      currentTime.setText(getCurrentTime(calendar));
    }

    private String getCurrentDate(Calendar calendar) {
      return calendar.get(Calendar.DAY_OF_MONTH) + "/"
          + (calendar.get(Calendar.MONTH) + 1) + "/"
          + calendar.get(Calendar.YEAR);
    }

    private String getTimeZone(Calendar calendar) {
      long gmtOffset = calendar.get(Calendar.ZONE_OFFSET); // offset from GMT in milliseconds
      String gmtOffsetString = String.valueOf(gmtOffset / 3600000);
      return (gmtOffset > 0) ? "GMT + " + gmtOffsetString : "GMT - " + gmtOffsetString;
    }

    private String getCurrentTime(Calendar calendar) {
      return getFormattedValue(calendar, Calendar.HOUR_OF_DAY) + ":" + getFormattedValue(calendar, Calendar.MINUTE);
    }

    private String getFormattedValue(Calendar calendar, int calendarField) {
      int value = calendar.get(calendarField);
      return StringUtils.leftPad(Integer.toString(value), 2, "0");
    }

    public JPanel getContentPanel() {
      return contentPanel;
    }

  }

}

```

# project_view_pane/README.md
# Project View Pane Demo [![JetBrains IntelliJ Platform SDK Docs](https://jb.gg/badges/docs.svg)][docs]
*Reference: [Project View in IntelliJ SDK Docs][docs:project_view]*

## Quickstart

The current demo describes an implementation of the `com.intellij.projectViewPane` extension point, which allows creating an additional presentation type for the Project view pane.
`ImagesProjectViewPane` limits the project tree to the images only.

### Extension Points

| Name                           | Implementation                                      | Extension Point Class     |
|--------------------------------|-----------------------------------------------------|---------------------------|
| `com.intellij.projectViewPane` | [ImagesProjectViewPane][file:ImagesProjectViewPane] | `AbstractProjectViewPane` |

*Reference: [Plugin Extension Points in IntelliJ SDK Docs][docs:ep]*


[docs]: https://plugins.jetbrains.com/docs/intellij/
[docs:project_view]: https://plugins.jetbrains.com/docs/intellij/project-view.html
[docs:ep]: https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html

[file:ImagesProjectViewPane]: ./src/main/java/org/intellij/sdk/view/pane/ImagesProjectViewPane.java


# project_view_pane/build.gradle.kts
```kotlin
// Copyright 2000-2024 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

plugins {
  id("java")
  id("org.jetbrains.intellij") version "1.17.4"
}

group = "org.intellij.sdk"
version = "2.0.0"

repositories {
  mavenCentral()
}

java {
  sourceCompatibility = JavaVersion.VERSION_17
}

// See https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html
intellij {
  version.set("2024.1.7")
}

tasks {
  buildSearchableOptions {
    enabled = false
  }

  patchPluginXml {
    version.set("${project.version}")
    sinceBuild.set("241")
    untilBuild.set("243.*")
  }
}

```

# project_view_pane/settings.gradle.kts
```kotlin
// Copyright 2000-2022 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.

rootProject.name = "project_view_pane"

```

# project_view_pane/.run/Run IDE with Plugin.run.xml
```xml
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Run Plugin" type="GradleRunConfiguration" factoryName="Gradle">
        <log_file alias="idea.log" path="$PROJECT_DIR$/build/idea-sandbox/system/log/idea.log"/>
        <ExternalSystemSettings>
            <option name="executionName"/>
            <option name="externalProjectPath" value="$PROJECT_DIR$"/>
            <option name="externalSystemIdString" value="GRADLE"/>
            <option name="scriptParameters" value=""/>
            <option name="taskDescriptions">
                <list/>
            </option>
            <option name="taskNames">
                <list>
                    <option value="runIde"/>
                </list>
            </option>
            <option name="vmOptions" value=""/>
        </ExternalSystemSettings>
        <ExternalSystemDebugServerProcess>true</ExternalSystemDebugServerProcess>
        <ExternalSystemReattachDebugProcess>true</ExternalSystemReattachDebugProcess>
        <DebugAllEnabled>false</DebugAllEnabled>
        <method v="2"/>
    </configuration>
</component>

```

# project_view_pane/src/main/resources/META-INF/plugin.xml
```xml
<!-- Copyright 2000-2023 JetBrains s.r.o. and other contributors. Use of this source code is governed by the Apache 2.0 license that can be found in the LICENSE file. -->
<!-- Plugin Configuration File. Read more: https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html -->

<idea-plugin>

  <!-- Unique id for this plugin. Must stay constant for the life of the plugin. -->
  <id>org.intellij.sdk.view.pane</id>

  <!-- Text to display as name on Settings | Plugin page -->
  <name>SDK: Project View Pane Demo</name>

  <!-- Product and plugin compatibility requirements -->
  <depends>com.intellij.modules.platform</depends>

  <!-- Text to display as description on Settings | Plugin page -->
  <description>
    <![CDATA[
      Demonstrates Project View Pane, listing only image files.
    ]]>
  </description>
  <change-notes>
    <![CDATA[
      <ul>
        <li><b>2.0.0</b> Convert to Gradle-based plugin</li>
        <li><b>1.0.0</b> Release 2018.3 and earlier.</li>
      </ul>
    ]]>
  </change-notes>

  <!-- Text to display as company information on Settings | Plugin page -->
  <vendor url="https://plugins.jetbrains.com">IntelliJ Platform SDK</vendor>

  <extensions defaultExtensionNs="com.intellij">
    <projectViewPane implementation="org.intellij.sdk.view.pane.ImagesProjectViewPane"/>
  </extensions>

</idea-plugin>

```

# project_view_pane/src/main/java/org/intellij/sdk/view/pane/ImagesProjectViewPane.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.
package org.intellij.sdk.view.pane;

import com.intellij.icons.AllIcons;
import com.intellij.ide.SelectInTarget;
import com.intellij.ide.impl.ProjectViewSelectInTarget;
import com.intellij.ide.projectView.ViewSettings;
import com.intellij.ide.projectView.impl.*;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.project.ProjectUtil;
import com.intellij.openapi.vfs.VirtualFile;
import org.jetbrains.annotations.NotNull;

import javax.swing.tree.DefaultTreeModel;

final class ImagesProjectViewPane extends ProjectViewPane {

  public static final String ID = "IMAGES";

  ImagesProjectViewPane(Project project) {
    super(project);
  }

  @NotNull
  @Override
  public String getTitle() {
    return "SDK Images";
  }

  @NotNull
  @Override
  public javax.swing.Icon getIcon() {
    return AllIcons.FileTypes.Custom;
  }

  @NotNull
  @Override
  public String getId() {
    return ID;
  }

  @Override
  public int getWeight() {
    return 10;
  }

  @NotNull
  @Override
  public SelectInTarget createSelectInTarget() {
    return new ProjectViewSelectInTarget(myProject) {

      @Override
      public String toString() {
        return ID;
      }

      @Override
      public String getMinorViewId() {
        return ID;
      }

      @Override
      public float getWeight() {
        return 10;
      }
    };
  }

  @NotNull
  @Override
  protected ProjectAbstractTreeStructureBase createStructure() {
    return new ProjectTreeStructure(myProject, ID) {
      @Override
      protected ImagesProjectNode createRoot(@NotNull Project project, @NotNull ViewSettings settings) {
        return new ImagesProjectNode(project, settings, getProjectDir(project), ImagesProjectViewPane.this);
      }

      @NotNull
      private static VirtualFile getProjectDir(Project project) {
        VirtualFile guessedProjectDir = ProjectUtil.guessProjectDir(project);
        if (guessedProjectDir == null) {
          throw new IllegalStateException("Could not get project directory");
        }
        return guessedProjectDir;
      }

      // Children will be searched in async mode
      @Override
      public boolean isToBuildChildrenInBackground(@NotNull Object element) {
        return true;
      }
    };
  }

  @NotNull
  @Override
  protected ProjectViewTree createTree(@NotNull DefaultTreeModel model) {
    return new ProjectViewTree(model) {
      @Override
      public boolean isRootVisible() {
        return true;
      }
    };
  }

}

```

# project_view_pane/src/main/java/org/intellij/sdk/view/pane/ImagesProjectNode.java
```java
// Copyright 2000-2023 JetBrains s.r.o. and contributors. Use of this source code is governed by the Apache 2.0 license.
package org.intellij.sdk.view.pane;

import com.intellij.icons.AllIcons;
import com.intellij.ide.projectView.PresentationData;
import com.intellij.ide.projectView.ProjectView;
import com.intellij.ide.projectView.ProjectViewNode;
import com.intellij.ide.projectView.ViewSettings;
import com.intellij.ide.projectView.impl.GroupByTypeComparator;
import com.intellij.ide.util.treeView.AbstractTreeNode;
import com.intellij.openapi.Disposable;
import com.intellij.openapi.application.ApplicationManager;
import com.intellij.openapi.application.ReadAction;
import com.intellij.openapi.fileEditor.FileEditorManager;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.project.ProjectUtil;
import com.intellij.openapi.roots.FileIndex;
import com.intellij.openapi.roots.ProjectRootManager;
import com.intellij.openapi.util.Key;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.openapi.vfs.VirtualFileManager;
import com.intellij.openapi.vfs.newvfs.BulkFileListener;
import com.intellij.openapi.vfs.newvfs.events.VFileEvent;
import com.intellij.psi.search.FilenameIndex;
import com.intellij.util.containers.ContainerUtil;
import com.intellij.util.ui.update.MergingUpdateQueue;
import com.intellij.util.ui.update.Update;
import org.jetbrains.annotations.NotNull;

import java.util.*;

public class ImagesProjectNode extends ProjectViewNode<VirtualFile> {

  private static final Key<Set<VirtualFile>> IMAGES_PROJECT_DIRS = Key.create("images.files.or.directories");

  private static final List<String> SUPPORTED_IMAGE_EXTENSIONS = List.of("jpg", "jpeg", "png", "svg");

  private final MergingUpdateQueue updateQueue;

  /**
   * Creates root node.
   */
  public ImagesProjectNode(@NotNull Project project,
                           @NotNull ViewSettings settings,
                           @NotNull VirtualFile rootDir,
                           @NotNull Disposable parentDisposable) {
    super(project, rootDir, settings);
    scanImages(project);
    setupImageFilesRefresher(project, parentDisposable); // subscribe to changes only in the root node
    updateQueue = new MergingUpdateQueue(ImagesProjectNode.class.getName(), 200, true, null, parentDisposable, null);
  }

  /**
   * Creates child node.
   */
  private ImagesProjectNode(@NotNull Project project,
                            @NotNull ViewSettings settings,
                            @NotNull VirtualFile file,
                            @NotNull MergingUpdateQueue updateQueue) {
    super(project, file, settings);
    this.updateQueue = updateQueue;
  }

  private void scanImages(@NotNull Project project) {
    for (String imageExtension : SUPPORTED_IMAGE_EXTENSIONS) {
      addAllByExt(project, imageExtension);
    }
  }

  private void addAllByExt(@NotNull Project project, @NotNull String extension) {
    Set<VirtualFile> imagesFiles = getImagesFiles(project);
    VirtualFile projectDir = ProjectUtil.guessProjectDir(project);
    Collection<VirtualFile> files = ReadAction.compute(() -> FilenameIndex.getAllFilesByExt(project, extension));
    for (VirtualFile file : files) {
      while (file != null && !file.equals(projectDir)) {
        imagesFiles.add(file);
        file = file.getParent();
      }
    }
  }

  @NotNull
  private Set<VirtualFile> getImagesFiles(@NotNull Project project) {
    Set<VirtualFile> files = project.getUserData(IMAGES_PROJECT_DIRS);
    if (files == null) {
      files = new HashSet<>();
      project.putUserData(IMAGES_PROJECT_DIRS, files);
    }
    return files;
  }

  private void setupImageFilesRefresher(@NotNull Project project, @NotNull Disposable parentDisposable) {
    project.getMessageBus().connect(parentDisposable)
        .subscribe(VirtualFileManager.VFS_CHANGES, new BulkFileListener() {
          @Override
          public void after(@NotNull List<? extends @NotNull VFileEvent> events) {
            boolean hasAnyImageUpdate = false;
            FileIndex fileIndex = ProjectRootManager.getInstance(project).getFileIndex();
            for (VFileEvent event : events) {
              VirtualFile file = event.getFile();
              if (file == null || !fileIndex.isInContent(file)) {
                continue;
              }
              String extension = file.getExtension();
              if (extension != null && SUPPORTED_IMAGE_EXTENSIONS.contains(extension)) {
                hasAnyImageUpdate = true;
                break;
              }
            }
            if (hasAnyImageUpdate) {
              updateQueue.queue(new Update("UpdateImages") {
                public void run() {
                  getImagesFiles(project).clear();
                  scanImages(project);
                  ApplicationManager.getApplication().invokeLater(() ->
                          ProjectView.getInstance(project)
                              .getProjectViewPaneById(ImagesProjectViewPane.ID)
                              .updateFromRoot(true),
                      project.getDisposed()
                  );
                }
              });
            }
          }
        });
  }

  @Override
  public boolean contains(@NotNull VirtualFile file) {
    return file.equals(getVirtualFile());
  }

  @Override
  @NotNull
  public VirtualFile getVirtualFile() {
    return getValue();
  }

  @NotNull
  @Override
  public Collection<? extends AbstractTreeNode<?>> getChildren() {
    List<VirtualFile> files = new ArrayList<>();
    for (VirtualFile file : getValue().getChildren()) {
      if (getImagesFiles(myProject).contains(file)) {
        files.add(file);
      }
    }
    if (files.isEmpty()) {
      return Collections.emptyList();
    }
    ViewSettings settings = getSettings();
    return ContainerUtil.sorted(
        ContainerUtil.map(files, (file) -> new ImagesProjectNode(myProject, settings, file, updateQueue)),
        new GroupByTypeComparator(myProject, ImagesProjectViewPane.ID));
  }

  @Override
  protected void update(@NotNull PresentationData data) {
    data.setIcon(getValue().isDirectory() ? AllIcons.Nodes.Folder : getValue().getFileType().getIcon());
    data.setPresentableText(getValue().getName());
  }

  @Override
  public boolean canNavigate() {
    return !getValue().isDirectory();
  }

  @Override
  public boolean canNavigateToSource() {
    return canNavigate();
  }

  @Override
  public void navigate(boolean requestFocus) {
    FileEditorManager.getInstance(myProject).openFile(getValue(), false);
  }

  @Override
  public int getTypeSortWeight(boolean sortByType) {
    // required for "Folder Always on Top"
    return getVirtualFile().isDirectory() ? 1 : 0;
  }

}

```
